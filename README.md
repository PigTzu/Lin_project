# Multi-timescale Neural Dynamics for Multisensory Integration in Autism Spectrum Condition
This is an ongoing project for Brainhack School 2026, which I try to do time-frequency analysis using MNE-Python. Dataset from [OpenNeuro ds006777](https://openneuro.org/datasets/ds006777/versions/1.0.0) would be used, and the entire processing/analyzing workflow and scripts will be updated.
## Background
- Our responses to multisensory stimuli typically differ from the combined responses of the corresponding unisensory stimuli. These integration effects are categorized as supra-additive (where the multisensory response exceeds the sum of unimodal responses) or sub-additive (where the combined effect is smaller).
- Larger alpha suppression serves as a marker for increased integration of information, indexing heightened integration load. This multisensory integration (MSI) effect extends beyond a mere summation of unimodal power responses alone[^1][^10].
- Different timescales, reflected in different oscillatory frequency bands, serve to route different information types through cortical networks[^2].
- Individuals with autism spectrum condition (ASC) exhibit an altered temporal window for MSI.; however few studies investigated MSI on this population through a multi-timescale approach.
## Research Aims
- Comparing the MSI effects (indexed by alpha suppression) between ASC and TD groups.
- Exploring the MSI effects across different frequency bands spatially and temporally.
## Dataset Description
- The dataset is sourced from OpenNeuro ds006777[^3], containing EEG data collected via a BioSemi system from both TD and ASC participants.
- Participants performed an audiovisual simple reaction-time task (AVSRT), consisting of three randomized trial types: visual-only (V), auditory-only (A), and simultaneous audiovisual (AV). Participants were instructed to press a response button as rapidly as possible upon detecting any stimulus.
## Data Analyses
EEG preprocessing and time-frequency analysis are performed using MNE-Python 1.12.1[^7][^8] and the [PyPREP](https://pyprep.readthedocs.io/en/stable/index.html)[^9] library to detect noisy channels.

It is recommended to create a folder named `code` in the project folder to store the scripts from this repository:
```
ds006777/                    
├── code/
│   ├── batch_prep_beh.py
│   ├── eeg_preprocessing_and_beh.ipynb
│   ├── time-frequency_analysis.ipynb
│   ├── functions.py
│   └── requirements.txt
├── sub-1501/
├── sub-1502/
├── ...
├── participants.tsv
├── dataset_description.json
└── ...
```
### How to run behavioral analysis and EEG preprocessing
- Both `eeg_preprocessing_and_beh_analysis.ipynb` and `batch_prep_beh.py` can be used for analyzing behavioral responses and preprocessing EEG data. Prior to execution, update the `base_dir` variable in the scripts to point to your local project directory.
- For `eeg_preprocessing_and_beh_analysis.ipynb`, you should specify which ONE subject you want to process in `subject_id`.
- For `batch_prep_beh.py`, you should specify which subject(s) to process in `subject_ids`. This script is mainly for processing multiple subjects without plotting functions.
- Upon executing the scripts, a subject-specific folder is created within `derivatives`. This folder contains the behavioral results (`sub-*_beh.csv`), the preprocessed epochs (`sub-*_eeg-epo.fif`), and a processing log (`sub-*_log.txt`).
```
ds006777/                    
├── code/
├── derivatives/           
│   ├── sub-10025/              
│   │   ├── sub-10025_beh.csv   
│   │   ├── sub-10025_eeg-epo.fif
│   │   └── sub-10025_log.txt
│   └── .../
```
**NOTE** 
- Make sure you have also downloaded the `functions.py` file (which contains user-defined functions) and put all these scripts in the same folder.
- The main differences between `eeg_preprocessing_and_beh_analysis.ipynb` and `batch_prep_beh.py` are that the former is mainly for processing one subject in which plotting functions could be used and code can be run cell by cell; the latter can be directly run in the terminal and is mainly for automatic batch processing for multiple subjects at once, so no plottings would be shown when running the script. 
- The script was developed under Linux (specifically, Windows Subsystem for Linux, WSL). To see interactive plottings, for Linux/WSL you can install a matplotlib backend Qt by running `pip install pyqt6` in the terminal. For other operating systems, you can refer to [MNE official website](https://mne.tools/stable/install/advanced.html) for more details.
### How to run time-frequency analysis
#### Renaming some folders and files
Prior to running the time-frequency analysis, it is important to understand the project structure and naming conventions. 

Subject folders with IDs beginning with `sub-10XXX` correspond to the TD group, whereas those beginning with `sub-11XXX` correspond to the ASC group. The analysis script uses these naming conventions to identify group membership automatically.

To complete the processes successfully, some subject folder names and corresponding preprocessed file (`-epo.fif`) names need to be changed in `derivatives`:
  - One ASC participant is stored under the folder name `sub-2713`. To ensure that the analysis scripts recognize this participant as belonging to the ASC group, rename both the subject folder (in `derivatives`) and the corresponding `.epo` file to `sub-112713`.
  - Participants who should be excluded from the analysis (e.g., due to poor behavioral performance) should be renamed by adding an `e` after `sub-`(also in `derivatives`), like:
  ```
  sub-2713   →  sub-112713
  sub-11976  →  sub-e11976
  ```
This naming convention prevents the scripts from processing excluded participants and ensures the correct sample size for subsequent analysis.

For the current implementation, folders and files of `sub-2713` and `sub-11976` have been renamed.
#### Computing and plotting time-frequency representations (TFR)
- The script `time-frequency_analysis.ipynb` should be used. As mentioned in the previous section, you also need to specify the project folder path in `base_dir`. 
- While running the "Sep up" section, a new folder `results` under `derivatives` will be created to store the grand-averaged output. It will also initialize a log file (`TFR_topomap_log.txt`) via MNE to keep track of the process.
- While running `compute_grand_tfr()`, the time-frequency-resolved power estimates for each subject at one condition will be calculated and saved to the corresponding subject folder under `derivatives` (e.g. `sub-10025_cond-V_eeg-tfr.h5`).
- After running all the cells, you will get six grand-averaged TFR files (e.g., `grand_AV_TD-tfr.h5`) stored in the `results` folder, topographic maps across five frequency bands for both group separately, and plottings of time-frequency representations across three experimental conditions.
```
ds006777/
├── code/                       
├── derivatives/            
│   ├── results/                
│   │   ├── grand_A_ASC-tfr.h5
│   │   ├── grand_A_TD-tfr.h5
│   │   ├── grand_AV_ASC-tfr.h5
│   │   ├── grand_AV_TD-tfr.h5
│   │   ├── grand_V_ASC-tfr.h5
│   │   ├── grand_V_TD-tfr.h5
│   │   └── TFR_topomap_log.txt  
│   ├── sub-10025/              
│   │   ├── sub-10025_beh.csv    
│   │   ├── sub-10025_cond-A_eeg-tfr.h5    
│   │   ├── sub-10025_cond-AV_eeg-tfr.h5     
│   │   ├── sub-10025_cond-V_eeg-tfr.h5   
│   │   ├── sub-10025_eeg-epo.fif 
│   │   └── sub-10025_log.txt  
│   └── .../      
```
**NOTE**
- Subjects without valid epoch files (due to noise exclusion during preprocessing) will log a failure message and be skipped safely (e.g., `sub-10129`, `sub-10170`, etc.), so no worries about the logging.
- Since the user-defined function `compute_grand_tfr()` takes several minutes (approx. 6.5 mins for TD, 11 mins for ASC), the grand-averaged TFR results are exported into the `results` folder as `-tfr.h5` files (e.g., `grand_AV_TD-tfr.h5`) for future instant loading. Therefore you don't need to run those cells to get the time-frequency-resolved power estimates every time you open the notebook, and just load the stored TFR files via `mne.time_frequency.read_tfrs()`!
## Results
A total of 22 TD and 38 ASC participants were analyzed. The figures below display the topographic maps across five frequency bands for ASC and TD groups respectively, and the time-frequency representations across three experimental conditions (AV, A, V) for both groups.
### Topographic maps for cross-modal conditions
![figures/topo_AV_ASC.png](https://github.com/PigTzu/Lin_project/blob/main/figures/topo_AV_ASC.png)
![figures/topo_AV_TD.png](https://github.com/PigTzu/Lin_project/blob/main/figures/topo_AV_TD.png)
### Time-frequency representations
![figures/TFR_2*3.png](https://github.com/PigTzu/Lin_project/blob/main/figures/TFR_2*3.png)
[^1]: Matyjek, M., Kita, S., Torralba Cuello, M., & Soto Faraco, S. (2024). Multisensory integration of speech and gestures in a naturalistic paradigm. Human brain mapping, 45(11), e26797.
[^2]: Senkowski, D., & Engel, A. K. (2024). Multi-timescale neural dynamics for multisensory integration. Nature Reviews Neuroscience, 25(9), 625-642.
[^3]: Theo Vanneau, John J. Foxe, Shlomit Beker, Daniella Cohen, Albulena Sejdu, and Sophie Molholm (2025). SFARI AVSRT EEG. OpenNeuro. [Dataset] doi: doi:10.18112/openneuro.ds006777.v1.0.0
[^4]: Vanneau, T., Foxe, J. J., Beker, S., & Molholm, S. (2025). Disrupted Top-Down Modulation as a Mechanism of Impaired Multisensory Processing in Children with an Autism Spectrum Diagnosis. bioRxiv, 2025-11.
[^5]: Matyjek, M., Kita, S., Cuello, M.T., & Faraco, S.S. (2025), Multisensory Integration of Naturalistic Speech and Gestures in Autistic Adults. Autism Research, 18: 1156-1169.
[^6]: Gao, C., Xie, W., Green, J. J., Wedell, D. H., Jia, X., Guo, C., & Shinkareva, S. V. (2021). Evoked and induced power oscillations linked to audiovisual integration of affect. Biological psychology, 158, 108006.
[^7]: Larson, E., Gramfort, A., Engemann, D. A., Leppakangas, J., Brodbeck, C., Jas, M., Brooks, T. L., Sassenhagen, J., McCloy, D., Luessi, M., King, J.-R., Höchenberger, R., Brunner, C., Goj, R., Favelier, G., van Vliet, M., Wronkiewicz, M., Appelhoff, S., Rockhill, A., … user27182. (2026). MNE-Python (v1.12.1). Zenodo. https://doi.org/10.5281/zenodo.19666955
[^8]: Gramfort, A., Luessi, M., Larson, E., Engemann, D. A., Strohmeier, D., Brodbeck, C., ... & Hämäläinen, M. (2013). MEG and EEG data analysis with MNE-Python. Frontiers in Neuroinformatics, 7, 267.
[^9]: Bigdely-Shamlo, N., Mullen, T., Kothe, C., Su, K. M., & Robbins, K. A. (2015). The PREP pipeline: standardized preprocessing for large-scale EEG analysis. Frontiers in neuroinformatics, 9, 16.
[^10]: Matyjek, M., Kita, S., Cuello, M. T., & Faraco, S. S. (2025). Multisensory integration of naturalistic speech and gestures in autistic adults. Autism Research, 18(6), 1156-1169.
