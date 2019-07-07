##########################################################################
#
#  This file is part of Lilith
#  v1 (2015) by Jeremy Bernon and Beranger Dumont 
#  v2 (2019) by Thi Nhung Dao, Sabine Kraml, Duc Ninh Le, Loc Tran Quang 
#
#  Web page: http://lpsc.in2p3.fr/projects-th/lilith/
#
#  In case of questions email sabine.kraml@lpsc.in2p3.fr 
#
#
#    Lilith is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Lilith is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Lilith.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################

import scipy.stats
from ..errors import OutputError, OuputIOError
from ..version import __version__

"""Write the XML and SLHA-like output in files."""

"""Initialize the reading of the user input from the XML input contained
        in the string inputstring."""


def couplings(couplings, filepath):
    """Write the couplings contained in self.couplings."""

    list_coup = ["tt", "bb", "tautau", "cc", "mumu", "WW", "ZZ", "VBF", "gammagamma",
                 "Zgamma", "gg_decay", "gg_prod_lhc8"]
    list_extra = ["BRinvisible", "BRundetected", "precision", "mass"]

    couplingdict = []
    if not couplings: # couplings is empty
        raise OutputError('there are no couplings')

    for redCp in couplings:
        redCp_corres = {}
        try:
            for coupling in list_coup:
                redCp_corres[coupling] = redCp[coupling]
            for extra in list_extra:
                redCp_corres[extra] = redCp["extra"][extra]
        except KeyError as s:
            raise OutputError('information is missing in reduced couplings:' +
                              str(s) + ' key is missing')
        if "name" in redCp["extra"]:
            redCp_corres["part"] = ' part="' + redCp["extra"]["name"] + '"'
        else:
            redCp_corres["part"] = ""

        couplingdict.append(redCp_corres)


    try:
        with open(filepath, "w") as f:
            f.write("""<?xml version="1.0"?>

<!--
input file for Lilith generated by Lilith {}
-->

<lilithinput>
""".format(__version__))

            for redCp_corres in couplingdict:
                f.write("""<reducedcouplings{part}>
  <mass>{mass}</mass>

  <C to="tt">{tt}</C>
  <C to="bb">{bb}</C>
  <C to="tautau">{tautau}</C>
  <C to="cc">{cc}</C>
  <C to="mumu">{mumu}</C>
  <C to="WW">{WW}</C>
  <C to="ZZ">{ZZ}</C>
  <C to="VBF">{VBF}</C>
  <C to="gammagamma">{gammagamma}</C>
  <C to="Zgamma">{Zgamma}</C>
  <C to="gg" for="decay">{gg_decay}</C>
  <C to="gg" for="prod">{gg_prod_lhc8}</C>

  <extraBR>
    <BR type="invisible">{BRinvisible}</BR>
    <BR type="undetected">{BRundetected}</BR>
  </extraBR>

  <precision>{precision}</precision>
</reducedcouplings>

""".format(**redCp_corres))

            f.write("</lilithinput>\n")
    except IOError as e:
        raise OuputIOError(
            'I/O error({0}): {1}'.format(e.errno, e.strerror) + '; cannot' +
            ' write in the output file "' + filepath + '".')


def signalstrengths(mu, filepath):
    """Write the signal strengths contained in user_mu or user_mu_tot."""
    
    list_prod = ["ggH", "VBF", "WH", "qqZH", "ggZH", "ttH", "tHq", "tHW", "bbH"]
    list_decay = ["bb", "tautau", "cc", "mumu", "WW", "ZZ", "Zgamma", "gammagamma", "gg", "invisible"]

    list_proddecay = []
    for prod in list_prod:
        for decay in list_decay:
            list_proddecay.append((prod,decay))
    
    try:
        if type(mu) is list:
            for mup in mu:
                for proddecay in list_proddecay:
                    mup[proddecay]
        else:
                for proddecay in list_proddecay:
                    mu[proddecay]
    except KeyError as s:
            raise OutputError('information is missing in signal strength:' +
                              str(s) + ' key is missing')


    if type(mu) is list:
        # coresponds to user_mu
        try:
            with open(filepath,"wb") as f:
                f.write("""<?xml version="1.0"?>

<!--
input file for Lilith generated by Lilith {}
-->

<lilithinput>
""".format(__version__))
            
                for mup in mu:
                    if "name" in mup["extra"]:
                        f.write("""<signalstrengths part="{}">
""".format(mup["extra"]["name"]))
                    else:
                        f.write("""<signalstrengths>
""")
                    f.write("""   <mass>{}</mass>
""".format(mup["extra"]["mass"]))
                    for prod, decay in list_proddecay:
                        if decay == "invisible":
                            f.write("""   <redxsBR prod="{0}" decay="{1}">{2}</redxsBR>
""".format(prod, decay, mup[(prod,decay)]))
                        else:
                            f.write("""   <mu prod="{0}" decay="{1}">{2}</mu>
""".format(prod, decay, mup[(prod,decay)]))
                    f.write("""</signalstrengths>
                    
""")
                f.write("""</lilithinput>""")


        except IOError as e:
            raise OuputIOError(
            'I/O error({0}): {1}'.format(e.errno, e.strerror) + '; cannot' +
            ' write in the output file "' + filepath + '".')

    else:
        # corresponds to user_mu_tot
        try:
            with open(filepath,"wb") as f:
                f.write("""<?xml version="1.0"?>

<!--
input file for Lilith generated by Lilith {}
-->

<lilithinput>
""".format(__version__))
            
                f.write("""<signalstrengths part="total">
""")
                for prod in list_prod:
                    for decay in list_decay:
                        if decay == "invisible":
                            f.write("""   <redxsBR prod="{0}" decay="{1}">{2}</redxsBR>
""".format(prod, decay, mu[(prod,decay)]))
                        else:
                            f.write("""   <mu prod="{0}" decay="{1}">{2}</mu>
""".format(prod, decay, mu[(prod,decay)]))
                f.write("""</signalstrengths>
                
""")
                f.write("""</lilithinput>""")


        except IOError as e:
            raise OuputIOError(
            'I/O error({0}): {1}'.format(e.errno, e.strerror) + '; cannot' +
            ' write in the output file "' + filepath + '".')


def results_xml(results, l, lilithversion, dbversion, filepath):
    """Write the results after likelihood calculation in XML format."""
    try:
        exp_ndf = 0
        with open(filepath,'wb') as f:
            f.write("""<lilithresults>
            
""")
            f.write("""  <lilithversion>{}</lilithversion>
""".format(lilithversion))
            f.write("""  <dbversion>{}</dbversion>
            
""".format(dbversion))
            for result in results:
                exp_ndf += int(result["dim"])
                x = result["eff"]["x"]
                if "y" in result["eff"]:
                    y = result["eff"]["y"]
                else:
                    y = {}

                f.write("""  <analysis experiment="{}" source="{}">
""".format(result["experiment"], result["source"]))
                if result["dim"] == 2:
                    f.write("""    <expmu decay="{}" dim="{}" type="{}">
""".format(x.keys()[0][-1], result["dim"], result["type"]))
                    for key, val in x.items():
                        f.write("""      <eff axis="x" prod="{}">{}</eff>
""".format(key[0], val))
                    for key, val in y.items():
                        f.write("""      <eff axis="y" prod="{}">{}</eff>
""".format(key[0], val))
                    f.write("""    </expmu>
""")
                if result["dim"] == 1:
                    if len(x.keys()) == 1:
                        f.write("""    <expmu decay="{}" dim="{}" type="{}">
""".format(x.keys()[0][-1], result["dim"], result["type"]))
                        f.write("""      <eff prod="{}">{}</eff>
""".format(x.keys()[0][0], x.values()[0]))
                        f.write("""    </expmu>
""")
                    else:
                        match = True
                        for key, val in x.items():
                            if key[-1]!=x.keys()[0][-1]: match = False
                        if match:
                            f.write("""    <expmu decay="{}" dim="{}" type="{}">
""".format(x.keys()[0][-1], result["dim"], result["type"]))
                            for key, val in x.items():
                                f.write("""      <eff prod="{}">{}</eff>
""".format(key[0], val))
                            f.write("""    </expmu>
""")
                        else:
                            f.write("""    <expmu dim="{}" type="{}">
""".format(result["dim"], result["type"]))
                            for key, val in x.items():
                                f.write("""      <eff prod="{}" decay="{}">{}</eff>
""".format(key[0],key[1],val))
                            f.write("""    </expmu>
""")

                f.write("""    <l>{}</l>
""".format(result["l"]))
                f.write("""  </analysis>

""")
            f.write(""" <ltot>{}</ltot>
""".format(l))
            f.write(""" <exp_ndf>{}</exp_ndf>

""".format(exp_ndf))
            f.write("""</lilithresults>
""")
        
    except IOError as e:
            raise OuputIOError(
            'I/O error({0}): {1}'.format(e.errno, e.strerror) + '; cannot' +
            ' write in the output file "' + filepath + '".')

def results_slha(results, l, l_SM, filepath):
    """Write the results after likelihood calculation in SLHA-like format."""
    exp_ndf = 0
    for result in results:
            exp_ndf += int(result["dim"])
    with open(filepath, "w") as f:
        f.write("BLOCK         LilithResults\n")
        f.write("  0           "+str(round(l,4))+"           # -2*LogL\n")
        f.write("  1           "+str(exp_ndf)+"                # exp_ndf\n")
        f.write("  2           "+str(round(l_SM,4))+"           # -2*LogL_SM\n")

def results_slha_pvalue(results, l, l_ref, ndf, filepath, db):
    """Write the results after likelihood calculation in SLHA-like format."""
    pvalue = 1-scipy.stats.chi2.cdf(l-l_ref, ndf)
    exp_ndf = 0
    for result in results:
            exp_ndf += int(result["dim"])
    with open(filepath, "w") as f:
        f.write("BLOCK         LilithResults\n")
        f.write("  0           "+str(round(l,4))+"           # -2*LogL\n")
        f.write("  1           "+str(exp_ndf)+"                # exp_ndf\n")
        f.write("  2           "+str(round(l_ref,4))+"           # -2*LogL_ref\n")
        f.write("  3           "+str(ndf)+"                 # fit_ndf\n")
        f.write("  4           "+str(round(pvalue,4))+"            # pvalue\n")
        f.write("  5           "+str(db)+"            # database version\n")


