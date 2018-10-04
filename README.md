<<<<<<< HEAD
############# A light framework for VHcc analysis. #############

The framework is composed of following scripts and designed to run the scripts in this order.

	A. 1_doBSubmit.py
		This script is for submitting LSF jobs to creat flat ntuple. It will excute Zllhcc.py

	B. 2_doBSubmit_reSubmit.py
		Once the submitted jobs finish, you can check if the jobs were properly completed and there were some errors. 
		This script will automatically detect problems from the logs, remove the ntuple, and resubmit the problematic jobs

	C. 3_doHadd.py
		This script perform Hadd for the ntuple and create a root file per process.

	D. 4_Zllhcc_template.py
		will create template from the hadded ntuple. All the weights are saved in VHcc_Weights.py

	E. 5_Zllhcc_plotting.py
		will produce histograms with Data/MC ratio		 

=======
# VHcc_light
############# A light framework for VHcc analysis #############

The framework is composed of following scripts and designed to run the scripts in this order.

        A. 1_doBSubmit.py
                This script is for submitting LSF jobs to create flat ntuple. It will excute Zllhcc.py

        B. 2_doBSubmit_reSubmit.py
                Once the submitted jobs finish, you can check if the jobs were properly completed and there were some errors.
                This script will automatically detect problems from the logs, remove the ntuple, and resubmit the problematic jobs

        C. 3_doHadd.py
                This script perform Hadd for the ntuple and create a root file per process.

        D. 4_Zllhcc_template.py
                will create template from the hadded ntuple. All the weights are saved in VHcc_Weights.py

        E. 5_Zllhcc_plotting.py
                will produce histograms with Data/MC ratio
>>>>>>> d2e03f0b574b89fcf0315b63bcd2bfc1c1c407dc
