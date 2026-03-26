import sys
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import zlib
import argparse
from ete4 import PhyloTree
from ete4.smartview import Layout, TextFace, SeqFace
from ete4.parser.fasta import read_fasta

def decompress_stream(stream):
    o = zlib.decompressobj(16 + zlib.MAX_WBITS)
    for chunk in stream:
        yield o.decompress(chunk)
    yield o.flush()

def get_fasta(taxids, pfams):
    def sp_url(taxids):
        url_tax = '+OR+'.join(['%%28taxonomy_id%%3A%s%%29' % taxid \
            for taxid in taxids])
        return url_tax

    def pf_url(pfams):
        url_pfam = '+AND+'.join(['%%28xref%%3Apfam-%s%%29' % pfam \
            for pfam in pfams])
        return url_pfam
    
    cmd_taxid = sp_url(taxids)
    cmd_pfams = pf_url(pfams)
    url_search = ('https://rest.uniprot.org/uniprotkb/stream?format=fasta&'
                  'query=%%28%%28%s%%29'
                  '+AND+'
                  '%%28keyword%%3AKW-1185%%29'
                  '+AND+'
                  '%s%%29' % (cmd_taxid, cmd_pfams))
    print('INFO--Search url:', url_search)
    return requests.get(url_search).text

def get_proteomeids_from_url(taxids):
    cmd_upid = '+OR+'.join(['%%28taxonomy_id%%3A%s%%29' % taxid for taxid in taxids])# if "OX=%s " % taxid in fasta])
    #print(cmd_upid)
    url_upid = ('https://rest.uniprot.org/proteomes/stream?'
                'fields=upid%%2Corganism_id%%2Clineage&'
                'format=tsv&'
                'query=%%28%%28%s%%29'
                '+AND+'
                '%%28proteome_type%%3A1%%29%%29' % cmd_upid)
    #print(url_upid)
    
    proteomeids = requests.get(url_upid).text
    #print(proteomeids)

    upid2taxid2lineage = [(line.split()[0], line.split()[1], line.split("\t")[2].split(",")[1].strip()) \
        for line in proteomeids.split("\n")[1:] \
            if line]
    
    return upid2taxid2lineage
        
def get_canonical_ids_from_url(upid2taxid2lineage):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    canonical_acs = []
    for upid, taxid, domain in upid2taxid2lineage:
        url_ref = ('https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/'
                   '%s/%s/%s_%s.fasta.gz' % (domain, upid, upid, taxid))
        r = session.get(url_ref, stream=False, verify=False, timeout=10)
        print("%s processd" % upid)
        #r = requests.get(url_ref, stream=False)
        canonical_acs += [header.split('|')[1] \
            for header in "".join([str(el) \
                for el in decompress_stream(r.iter_content(1024))]).split(">") \
                    if len(header.split("|")) > 1]
        
    return canonical_acs

def get_canonical_ids_from_local(upid2taxid2lineage, 
                                 path="/mnt/cglab.shared/Data/DBs/Uniprot/Reference_Proteomes_2024/"):

    canonical_acs = []
    for upid, taxid, domain in upid2taxid2lineage:
        filename_proteome = '%s/%s/%s_%s.fasta.gz' % (domain, upid, upid, taxid)
        #print(path+filename_proteome)
        # Quick fix, bug in ete4
        # /opt/conda/envs/phylo/lib/python3.12/site-packages/ete4/parser/fasta.py
        if not os.path.isfile(path+filename_proteome):
            print("INFO--MISSING-", path+filename_proteome)
            continue
        
        unzipped = './%s_%s.fasta' % (upid, taxid)
        os.system("zcat %s > %s" % (path+filename_proteome, unzipped))
        #os.system("cp %s ./" % (path+filename_proteome))
        #os.system("gunzip %s_%s.fasta.gz" % (upid, taxid))
        
        
        #print(unzipped)
        Fprot = read_fasta(unzipped, fix_duplicates=False)
        
        os.system("rm %s" % unzipped)
        
        canonical_acs += [header.split('|')[1] for header in Fprot.name2id]
        
    return canonical_acs


def get_from_local(infile, pfams):
    for pfam in pfams:
        os.system("wget -O %s.hmm.gz 'https://www.ebi.ac.uk/interpro/wwwapi//entry/pfam/%s?annotation=hmm'" % (pfam, pfam))
        os.system("gunzip %s.hmm.gz" % pfam)
        os.system("cat %s.hmm >> %s.hmm" % (pfam, "_".join(pfams)))
    os.system("hmmsearch --cpu %s --cut_ga -o /dev/null --tblout hmmsearch.tblout %s.hmm %s" % (args['cpu'], "_".join(pfams), infile))
    seqids = []
    for line in open("hmmsearch.tblout"):
        if line.startswith("#"):
            continue
        seqids.append(line.split()[0])
    F = read_fasta(infile, fix_duplicates=False)
    seqids = set(seqids)
    print("INFO--Retrieved %s local sequences" % len(seqids))
    fasta = "\n".join([">%s\n%s" % (seqid, F.get_seq(seqid)) for seqid in seqids])
    return fasta
    
def get_seqs(fastafile):
    """Read a fasta file and return a dict with d[description] = sequence.

    Example output: {'Phy003I7ZJ_CHICK': 'TMSQFNFSSAPAGGGFSFSTPKT...', ...}
    """
    name2seq = {}
    seq = ''
    for line in open(fastafile):
        if line.startswith('>'):
            if seq:
                name2seq[head] = seq
                seq = ''
                head = line.lstrip('>').rstrip()
            else:
                head = line.lstrip('>').rstrip()
        else:
            seq += line.rstrip()
    name2seq[head] = seq
    return name2seq

def layout_alnface_gray(node):
    if node.is_leaf:

        seq_face = SeqFace(
            seq,
            seqtype='aa', gap_format='line', seq_format='[]',
            width=800, height=None,
            fgcolor='black', bgcolor='#bcc3d0', gapcolor='gray',
            gap_linewidth=0.2,
            max_fsize=12, ftype='sans-serif',
            padding_x=0, padding_y=0)

        node.add_face(seq_face, position='aligned')
    return

def layout_alnface_compact(node):
    if node.is_leaf:
        seq = node.props.get('seq')
        if args['positions']:
            seq = "".join([seq[int(n)-1] for n in args['positions'].split(",")])        
        seq_face = SeqFace(
            seq,
            seqtype='aa', gap_format='line', seq_format='compactseq',
            width=800, height=None,
            fgcolor='black', bgcolor='#bcc3d0', gapcolor='gray',
            gap_linewidth=0.2,
            max_fsize=12, ftype='sans-serif',
            padding_x=0, padding_y=0)

        node.add_face(seq_face, position='aligned')
    return

def layout_seqface(node):
    if node.is_leaf:
        seq = node.props.get('seq')
        if args['positions']:
            seq = "".join([seq[int(n)-1] for n in args['positions'].split(",")])        
        return [SeqFace(seq, seqtype='aa',poswidth=15, position='aligned')]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Uniprot/Pfam-based protein family evolution analysis')
    parser.add_argument('--pfam', help='Comma-separated  Pfam domain ids e.g. PF00001,PF00002', \
        required=True, type=str, default='PF01094,PF00060')
    parser.add_argument('--taxids', help='Comma-separated taxids OR taxids list path', \
        required=False, type=str)#, default='10090,9606,7227')
    parser.add_argument('--cpu', help='Number of threads', \
        type=str, default='32')
    parser.add_argument('--ml', help='ML program 2 use', \
        type=str, default="fasttree", choices=['fasttree','iqtree'])
    parser.add_argument('--aln', help='Aligning algorithm 2 use', \
        type=str, default="mafft", choices=['mafft','einsi','clustalo'])
    parser.add_argument('--gt', help='-gt parameter of trimal', \
        type=str, default="0.1")
    parser.add_argument('--colormap', help='Taxid 2 color map path (tab-delim)', \
        required=False, type=str)
    parser.add_argument('--local_fasta', help='Comma-separated paths of fasta 2 search', \
        required=False, type=str)
    parser.add_argument('--MSA', help='Path of MSA', \
        action='store_true')
    parser.add_argument('--positions', help='Comma-separated alignment positions', \
        required=False, type=str)                
    parser.add_argument('--prefix', help='Prefix for output files', \
        required=True, type=str)
    parser.add_argument('--port', help='Port for tree server', \
        required=False, type=int, default='5001')    
    
    # args as dict containing the arguments
    args = vars(parser.parse_args())
    
    print("INFO--Processing Pfam domains:", args['pfam'])
    pfams = args['pfam'].split(',')
    if type(args['taxids']) == str:
        if os.path.isfile(args['taxids']):
            taxids = [line.strip().split()[0] for line in open(args['taxids']) if not line.startswith('#')]
            #taxids = [line.strip().split()[-1] for line in open(args['taxids']).readlines()[1:]]
        else:
            try:
                taxids = args['taxids'].split(',')
                print('Taxids loaded from command line')
            except:
                raise('Taxids should be comma-separated or path')
            
        print("INFO--Processing Taxids:", ",".join(taxids))
    else:
        taxids = None
        if args['local_fasta']:
            print("INFO--Processing only from local, hopefully")
   
    #F = read_fasta(get_fasta(taxids=taxids, pfams=pfams)) 
    # print("INFO--Retrieved", len(F), "sequences")

    
    try:
        print('Colormap parsing')
        colormap = {line.split()[0]:line.split()[1].strip() for line in open(args['colormap']).readlines() if line}
        print('Colormap OK')
    except:
        pass
        
    seqid2gene = None
    
    #filename_fasta = "%s.%s.fa" % ("_".join(pfams), "_".join(taxids))
    filename_fasta = "%s.fa" % args['prefix']

    if os.path.isfile(filename_fasta):
        print("INFO--Fasta already present")
        filename_seqid2name = filename_fasta.replace(".fa", ".seqid2gname.tab")
        if os.path.isfile(filename_seqid2name):
            seqid2gene = {}
            for line in open(filename_seqid2name):
                f = line.strip().split('\t')
                seqid2gene[f[0]] = f[1]
    else:
        if taxids:
            fasta = get_fasta(taxids=taxids, pfams=pfams)
            print("INFO--Retrieved Total", fasta.count(">"), "sequences")
            
            out = open(filename_fasta, "w")
            # Load Fasta and keep
            F = read_fasta(fasta, fix_duplicates=False)
            taxids_found = set([header.split("OX=")[1].split()[0] for header in F.name2id])
            
            # Check that, taxids vs taxids_found
            # upid2taxid2lineage = (get_proteomeids_from_url(taxids=taxids_found))
            upid2taxid2lineage = (get_proteomeids_from_url(taxids=taxids))

            print('INFO--Processing', len(upid2taxid2lineage), "species' data")

            canonical_acs = get_canonical_ids_from_local(upid2taxid2lineage)
            
            seqid2gene = {}
            for header in F.name2id:
                ac = header.split("|")[1]
                if not ac in canonical_acs:
                    continue
                taxid = header.split("OX=")[1].split()[0]
                seqid = "%s.%s" % (taxid, ac)
                print(">%s" % seqid, file=out)
                print(F.get_seq(header), file=out)
                try:
                    genename = header.split("GN=")[1].split()[0]
                    seqid2gene[seqid] = genename
                except IndexError:
                    seqid2gene[seqid] = header.split("|")[2].split()[0]
                    
            out.close()
            
            filename_seqid2name = filename_fasta.replace(".fa", ".seqid2gname.tab")
            out = open(filename_seqid2name, 'w')
            for seqid in seqid2gene:
                print('%s\t%s' % (seqid, seqid2gene[seqid]), file=out)
            out.close()
        
        if args['local_fasta']:
            #new_filename = filename_fasta.replace(".fa", ".plus_local.fa")
            #os.system("mv %s %s" % (filename_fasta, new_filename))
            #filename_fasta = new_filename
            out = open(filename_fasta, "a")
            if os.path.isfile('local.fa'):
                os.system("rm local.fa")
            for local in args['local_fasta'].split(","):
                os.system("cat %s >> local.fa" % local)
            fasta = get_from_local("local.fa", pfams)
            print(fasta, file=out)
            out.close()
            os.system("rm local.fa")
        
        #print("INFO--Number of canonical sequences:", len(seqid2gene))
    if args['cpu'] == 'AUTO':
        aln_cpu = 32
    else:
        aln_cpu = args['cpu']
    if args['aln'] == 'mafft':
        filename_aln = filename_fasta.replace(".fa", ".mft")
        if os.path.isfile(filename_aln):
            print("INFO--MSA precomputed")
        else:
            print("INFO--Computing MSA")
            os.system("mafft --quiet --thread %s %s > %s" % (aln_cpu, filename_fasta, filename_aln))
            print("INFO--Trimming")
            filename_trimal = filename_aln+".gt%s" % args['gt'].replace(".","")
            os.system("trimal -in %s -out %s -gt %s" % (filename_aln, filename_trimal, args['gt']))
    elif args['aln'] == 'einsi':
        filename_aln = filename_fasta.replace(".fa", ".einsi")
        if os.path.isfile(filename_aln):
            print("INFO--MSA precomputed")
        else:
            print("INFO--Computing MSA")
            os.system("einsi --thread %s %s > %s" % (aln_cpu, filename_fasta, filename_aln))    
            print("INFO--Trimming")
            filename_trimal = filename_aln+".gt%s" % args['gt'].replace(".","")
            os.system("trimal -in %s -out %s -gt %s" % (filename_aln, filename_trimal, args['gt']))
    elif args['aln'] == 'clustalo':
        filename_aln = filename_fasta.replace(".fa", ".clustalo")
        if os.path.isfile(filename_aln):
            print("INFO--MSA precomputed")
        else:
            print("INFO--Computing MSA")
            os.system("clustalo --threads %s -i %s -o %s" % (aln_cpu, filename_fasta, filename_aln))    
            print("INFO--Trimming")
            filename_trimal = filename_aln+".gt%s" % args['gt'].replace(".","")
            os.system("trimal -in %s -out %s -gt %s" % (filename_aln, filename_trimal, args['gt']))            

    filename_trimal = filename_aln+".gt%s" % args['gt'].replace(".","")

    if args['ml'] == 'fasttree':
        filename_tree = filename_trimal+".lg.fasttree"
        if os.path.isfile(filename_tree):
            print("INFO--Phylogenetic tree precomputed")
        else:
            print("INFO--Computing Phylogenetic tree")
            os.system("fasttree -lg %s > %s" % (filename_trimal, filename_tree))
    elif args['ml'] == 'iqtree':
        filename_tree = filename_trimal+".treefile"
        if os.path.isfile(filename_tree):
            print("INFO--Phylogenetic tree precomputed")
        else:
            print("INFO--Computing Phylogenetic tree")
            os.system("iqtree -s %s --prefix %s -mset LG -B 1000 -T %s" % (filename_trimal, filename_trimal, args['cpu']))
            #os.system("iqtree -s %s --prefix %s -m LG+R8 -alrt 1000 -T %s" % (filename_trimal, filename_trimal, args['cpu']))
            #os.system("iqtree -s %s --prefix %s -m MFP -T %s" % (filename_trimal, filename_trimal, args['cpu']))
        
#fasttree -quiet -lg %s > %s" % (filename_aln, filename_fasttree))

    print("INFO--Loading tree in %s" % filename_tree)

    # ETE4 functions

    # tree
    def tree_modify_style(tree_style):
        tree_style.collapse_size = 1
        tree_style.smartzoom = False

    # node
    def node_names_style(node):
        if node.is_leaf:
            return [TextFace(node.name.split(".")[1], style={'fill':"black"}, column=0, position='right'),
                    TextFace("(%s)" % node.props['gene_name'], style={'fill':"darkgray"}, column=1, position='right'),
                    TextFace("(%s)" % node.props['sci_name'], style={'fill':"darkgray"}, column=2, position='right')]

    def node_color_style(node):        
        if 'color' in node.props:
            # Branch lines (horizontal lines) will be brown and dashed, and 10 pixels thick.
            style_line = {'stroke-width': 3 ,
                          'stroke': node.props['color']}
            return {'hz-line': style_line,
                    'vt-line': style_line}


    def node_evo_style(node):
        if 'evoltype' in node.props and node.props['evoltype'] == 'D':
            style_dot = {'shape': 'triangle',
                         'radius': 10,
                         'fill': 'red'}
            return {'dot': style_dot}
    
    t = PhyloTree(open(filename_tree), 
                  sp_naming_function=lambda node: node.name.split('.')[0])
    
    t.set_outgroup(t.get_midpoint_outgroup())
    t.resolve_polytomy(descendants=True)
    t.annotate_ncbi_taxa()
    _events = t.get_descendant_evol_events()
    
    for node in t.traverse():
        if 'colormap' in args:
            for taxid in node.props['lineage'][::-1]:
                if str(taxid) in colormap:
                    node.add_prop("color", colormap[str(taxid)])
                    break
        if node.is_leaf:
            if seqid2gene and node.name in seqid2gene:
                node.add_prop("gene_name", seqid2gene[node.name])
            else:
                node.add_prop("gene_name", "-")

    if args['MSA']:
        # get information alignment
        #MSA = filename_trimal
        MSA = filename_aln
        print(MSA)
        name2seq = get_seqs(MSA)

        for leaf in t:
            leaf.add_prop('seq', name2seq[leaf.name])

    if not args['MSA']:
        layouts = []
    else:
        print("INFO--MSA loaded")
        layouts = [
        #Layout(name='compact_aln', ns=layout_alnface_compact, aligned_faces=True),
        #Layout(name='gray_aln', ns=layout_alnface_gray, aligned_faces=True, active=False),
        Layout(name='seq', draw_node=layout_seqface, active=True)
        ]

    tree_layout = Layout(name="MyLayout", draw_tree=tree_modify_style, active=True)
    layouts.append(tree_layout)
    names_layout = Layout(name="Names", draw_node=node_names_style)
    layouts.append(names_layout)
    color_layout = Layout(name="Colors", draw_node=node_color_style)
    layouts.append(color_layout)
    evo_layout = Layout(name="Duplications", draw_node=node_evo_style, active=False)
    layouts.append(evo_layout)
    
    #ts = TreeStyle()
    #ts.show_leaf_name = False  # do not add leaf names again
    #ts.layout_fn = layouts
    
    t.explore(layouts=layouts, keep_server=True, quiet=True, port=args['port'], show_leaf_name=False, include_props=("name", "sci_name", "evoltype", "dist", "support"))
    #t.explore(layouts=layouts, keep_server=True, quiet=True, show_leaf_name=False, include_props=("name", "sci_name", "dist", "support"))
