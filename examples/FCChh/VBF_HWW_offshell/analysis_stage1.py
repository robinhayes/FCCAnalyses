'''
Analysis example for FCC-hh, using VBF HWW events 
'''
from argparse import ArgumentParser


# Mandatory: Analysis class where the user defines the operations on the
# dataframe.
class Analysis():
    '''
    Di-Higgs analysis in bbyy.
    '''
    def __init__(self, cmdline_args):
        parser = ArgumentParser(
            description='Additional analysis arguments',
            usage='Provide additional arguments after analysis script path')
        # Parse additional arguments not known to the FCCAnalyses parsers
        # All command line arguments know to fccanalysis are provided in the
        # `cmdline_arg` dictionary.
        self.ana_args, _ = parser.parse_known_args(cmdline_args['unknown'])

        # Mandatory: List of processes to run over
        self.process_list = {
            # # Add your processes like this: 
            ## '<name of process>':{'fraction':<fraction of events to run over>, 'chunks':<number of chunks to split the output into>, 'output':<name of the output file> }, 
            # # - <name of process> needs to correspond either the name of the input .root file, or the name of a directory containing root files 
            # # If you want to process only part of the events, split the output into chunks or give a different name to the output use the optional arguments
            # # or leave blank to use defaults = run the full statistics in one output file named the same as the process:
            'mgp8_pp_vbf_h01j_5f_hww': {'fraction':0.05},
        }

        # Mandatory: Input directory where to find the samples, or a production tag when running over the centrally produced
        # samples (this points to the yaml files for getting sample statistics)
        self.input_dir = '/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v06/II/'

        # Optional: output directory, default is local running directory
        self.output_dir = 'outputs/FCChh/VBF_HWW_offshell/presel/'

        # Optional: analysisName, default is ''
        self.analysis_name = 'FCC-hh VBF HWW offshell analysis'

        # Optional: number of threads to run on, default is 'all available'
        # self.n_threads = 4

        # Optional: running on HTCondor, default is False
        # self.run_batch = False

        # Optional: Use weighted events
        self.do_weighted = True 

        # Optional: read the input files with podio::DataSource 
        self.use_data_source = False # explicitly use old way in this version 

        # Optional: test file that is used if you run with the --test argument (fccanalysis run ./examples/FCChh/ggHH_bbyy/analysis_stage1.py --test)
        self.test_file = 'root://eospublic.cern.ch//eos/experiment/fcc/hh/' \
                         'generation/DelphesEvents/fcc_v06/II/mgp8_pp_vbf_h01j_5f_hww' \
                         'events_000000001.root'


    # Mandatory: analyzers function to define the analysis graph, please make
    # sure you return the dataframe, in this example it is dframe2
    def analyzers(self, dframe):
        '''
        Analysis graph.
        '''
        dframe2 = (
            dframe

            ########################################### DEFINITION OF VARIABLES ########################################### 

            # generator event weight
            .Define("weight",  "EventHeader.weight")

            ########################################### HIGGS ########################################### 

            .Define("mc_particles", "Particle")
            .Define("mc_Higgs", "FCCAnalyses::MCParticle::sel_pdgID(25, true)(mc_particles)")
            .Define("n_mc_Higgs", "FCCAnalyses::MCParticle::get_n(mc_Higgs)")
            .Define("m_H",  "FCCAnalyses::MCParticle::get_mass(mc_Higgs)[0]")
        
            # Attempt at getting only Higgs that decay to WW, but didn't work. Some issue with the "ZZ" string (would need to modify function to take WW later but just tried this first)
            # .Alias("mc_daughters", "_Particle_daughters.index")

            # .Define("mc_Higgs_final", "AnalysisFCChh::get_truth_Higgs(mc_Higgs, mc_daughters, 'ZZ')") # retrieves the leading pT pair of all possible
            # .Define("n_mc_Higgs_final", "FCCAnalyses::MCParticle::get_n(mc_Higgs)")
            # .Define("m_H_final",  "FCCAnalyses::MCParticle::get_mass(mc_Higgs_final)[0]")
            ########################################### APPLY PRE-SELECTION ########################################### 
            # lines like:
            #.Filter("n_gamma > 1")
            #.Filter("n_bjets > 1")

        )
        return dframe2

    # Mandatory: output function, please make sure you return the branch list
    # as a python list
    def output(self):
        '''
        Output variables which will be saved to output root file.
        '''
        branch_list = [
            'weight',
            # Higgs:
            'n_mc_Higgs', 'm_H', 
            #'n_mc_Higgs_final', 'm_H_final',
        ]
        return branch_list
