import mne
import numpy as np
import pandas as pd
import os
import glob
import gc
from functions import mark_bad_channels

print('The MNE-Python version in this script is 1.12.1. Please check whether your MNE version matches, and if is too old, then please modify the parameters based on official documentation.')
print('Your MNE version:',mne.__version__)

#%%
# To use the code, modify base_dir to your project folder path.
base_dir = '/home/p2894/mne_eeg_workshop/ds006777'
derivatives_dir = os.path.join(base_dir, 'derivatives')

if not os.path.exists(derivatives_dir):
    os.makedirs(derivatives_dir)
    print(f"Has successfully created: {derivatives_dir}")
else:
    print("Folder `derivatives` exists. No need to create.")

subject_paths = glob.glob(os.path.join(base_dir, 'sub-*'))
subject_ids = sorted([os.path.basename(p) for p in subject_paths if os.path.isdir(p)])
# Or you can manually specify which subject to be processed:
#subject_ids = ['sub-2713']

print(f"List of subjects to be processed: {subject_ids}")
print(f'Totally {len(subject_ids)} will be processed.')
user_input = input("Are you ready to start processing these files? (y/n): ").strip().lower()
#%%
if user_input == 'y':
    print("Confirmation complete, ready to begin batch processing!\n")

    for subject_id in subject_ids:
        print(f"\n==================== Start to process: {subject_id} ====================")
        
        try:
            bdf_file_path = os.path.join(base_dir, subject_id, 'eeg', f'{subject_id}_task-AVSRT_run-01_eeg.bdf')
            subject_folder = os.path.join(derivatives_dir, subject_id)
            os.makedirs(subject_folder, exist_ok=True)
            
            log_file_path = os.path.join(subject_folder, f'{subject_id}_log.txt')
            mne.set_log_file(log_file_path, overwrite=True)
            
            if not os.path.exists(bdf_file_path):
                print(f"Cannot find {subject_id} .bdf file. Skip.")
                continue
            
            print('Importing raw file...')
            raw = mne.io.read_raw_bdf(bdf_file_path, preload=True)
            print('Raw file imported.')

            print('Looking for events...')
            events = mne.find_events(raw, shortest_event=1)
            print('Events found.')

            print('Setting montage and channel types...')
            montage = mne.channels.make_standard_montage('biosemi64')
            raw = raw.set_montage(montage, on_missing='ignore')
            raw.set_channel_types({"EXG1":"emg"})
            raw.set_channel_types({"EXG2":"emg"})
            raw.set_channel_types({"EXG3":"emg"})
            raw.set_channel_types({"EXG4":"emg"})
            raw.set_channel_types({"EXG5":"emg"})
            raw.set_channel_types({"EXG6":"emg"})
            raw.set_channel_types({"EXG7":"emg"})
            raw.set_channel_types({"EXG8":"emg"})
            print('Montage and channel types have been set.')

            print('Marking bad channels...')
            bads = mark_bad_channels(raw)
            raw.info['bads'] = bads
            print('Bad channels:', raw.info['bads'])
            print('Bad channels have been marked.')

            if len(raw.info['bads']) > len(raw.get_channel_types(picks=['eeg']))*0.15:
                print('Too many bad channels. The data should be discarded.')
                continue
            if 'Fp1' in raw.info['bads'] or 'Fp2' in raw.info['bads']:
                print(f"{subject_id}'s EOG-like channels (Fp1/Fp2) are damaged. Data processing for this subject is abandoned.")
                continue

            print('Re-referencing...')
            raw_ref = raw.set_eeg_reference(ref_channels='average')
            print('Average reference done.')

            # Create two independent copies of raw_ref to prevent simultaneous object mutation
            raw_for_ica = raw_ref.copy()
            raw_for_analysis = raw_ref.copy()

            print('ICA running...')
            # Preparation for ICA
            raw_for_ica = raw_for_ica.copy().filter(l_freq=1.0, h_freq=50.0)

            n_components = None
            random_state = 42
            method = 'fastica'
            fit_params = None
            max_iter = 1000
            
            ica = mne.preprocessing.ICA(n_components=n_components, method=method, max_iter=max_iter, fit_params=fit_params, random_state=random_state)
            
            picks_ica = mne.pick_types(raw_for_ica.info, eeg=True, eog=False, exclude="bads")
            ica.fit(raw_for_ica, picks=picks_ica)

            ica.exclude = []
            eog_indices, eog_scores = ica.find_bads_eog(raw_for_ica.copy(), ch_name=['Fp1', 'Fp2'])
            ica.exclude = eog_indices
            print('Components to be removed:',ica.exclude)
            
            ica.apply(raw_for_analysis)
            print('ICA done.')

            print('Filtering...')
            raw_for_analysis = raw_for_analysis.copy().filter(l_freq=0.05, h_freq=50)
            print('Data have been filtered.')

            # Rename events with bad responses & behavioral analysis (RT)
            print('Analyzing behavioral responses (RT)...')
            sfreq = raw.info['sfreq']

            events_news = events.copy()
            events_news = events_news[np.where((events_news[:,2]==3) | (events_news[:,2]==4) | (events_news[:,2]==5) | (events_news[:,2]==1))]

            valid_rt_data = []

            stim_dict = {3: 'AV', 4: 'A', 5: 'V'}

            for i in range(len(events_news)):
                current_event = events_news[i, 2]
                
                if current_event in [3, 4, 5]:
                    
                    response_count = 0  
                    rt = 0.0          
                    
                
                    for j in range(i + 1, len(events_news)):
                        next_event = events_news[j, 2]
                        
                        if next_event in [3, 4, 5]:
                            break
                            
                        elif next_event == 1:
                            if response_count == 0:
                                rt = (events_news[j, 0] - events_news[i, 0]) / sfreq
                            
                            response_count += 1
                            
                    is_invalid = False
                    
                    if response_count == 0:
                        is_invalid = True
                    elif response_count > 1:
                        is_invalid = True 
                    else:
                        if rt < 0.1 or rt > 1.0:
                            is_invalid = True  
                            
                    if is_invalid:
                        events_news[i, 2] = current_event * 10
                    else:
                        valid_rt_data.append({
                            'Event_Index': i,               
                            'Stimulus_Type': stim_dict[current_event], 
                            'Reaction_Time': rt              
                        })
            
            # Epoching
            print('Extracting epochs, ignoring poor behavioral responses with baseline correction and PTP rejection...')
            events_epochs = events_news[np.where((events_news[:,2]==3) | (events_news[:,2]==4) | (events_news[:,2]==5) | (events_news[:,2]==30) | (events_news[:,2]==40) | (events_news[:,2]==50))]
            event_id = {"AV": 3, "A": 4, "V": 5}

            epochs = mne.Epochs(raw_for_analysis, events=events_epochs, event_id=event_id, tmin=-0.2, tmax=0.9, baseline=(-0.2, 0), reject=dict(eeg=200e-6), detrend=0, preload=True)

            # Behavioral analysis (hit rate)
            print('Analyzing behavioral responses (hit rate)...')
            av_good = len(np.where(events_news[:, 2] == 3)[0])
            av_bad  = len(np.where(events_news[:, 2] == 30)[0])
            av_total = av_good + av_bad
            av_hit_rate = (av_good / av_total) if av_total > 0 else np.nan
            
            a_good = len(np.where(events_news[:, 2] == 4)[0])
            a_bad  = len(np.where(events_news[:, 2] == 40)[0])
            a_total = a_good + a_bad
            a_hit_rate = (a_good / a_total) if a_total > 0 else np.nan
            
            v_good = len(np.where(events_news[:, 2] == 5)[0])
            v_bad  = len(np.where(events_news[:, 2] == 50)[0])
            v_total = v_good + v_bad
            v_hit_rate = (v_good / v_total) if v_total > 0 else np.nan

            data = {
                'Condition': ['AV', 'A', 'V'],
                'Good_Trials': [av_good, a_good, v_good],
                'Bad_Trials': [av_bad, a_bad, v_bad],
                'Total_Trials': [av_total, a_total, v_total],
                'Hit_Rate': [av_hit_rate, a_hit_rate, v_hit_rate]
            }
            df_summary = pd.DataFrame(data)
            df_summary['Hit_Rate_Percent'] = (df_summary['Hit_Rate'] * 100).round(2).astype(str) + '%'
            
            df_valid_rts = pd.DataFrame(valid_rt_data)
            mean_rts = df_valid_rts.groupby('Stimulus_Type')['Reaction_Time'].mean()
            df_summary['Mean_RT_Secs'] = df_summary['Condition'].map(mean_rts)
            print('Behavioral analyses done.')

            # Bad channels interpolation
            print('Interpolating bad channels...')
            epochs = epochs.copy().interpolate_bads()
            print('Bad channels interpolated.')

            # Save files to derivatives
            print('Saving files to derivatives...')
            beh_file_path = os.path.join(subject_folder, f'{subject_id}_beh.csv')
            df_summary.to_csv(beh_file_path, index=False)

            eeg_file_path = os.path.join(subject_folder, f'{subject_id}_eeg-epo.fif')
            epochs.save(eeg_file_path, overwrite=True)
            print(f'Three files - {subject_id}_beh.csv, {subject_id}_eeg-epo.fif, & {subject_id}_log.txt have been saved.')
            
            print(f"{subject_id} has been processed and saved successfully!")
        
        except Exception as e:
            print(f"{subject_id} fails to process! Reason: {e}")
            continue
        
        finally:
            if 'raw' in locals(): del raw
            if 'raw_ref' in locals(): del raw_ref
            if 'raw_for_ica' in locals(): del raw_for_ica
            if 'raw_for_analysis' in locals(): del raw_for_analysis
            if 'ica' in locals(): del ica
            if 'epochs' in locals(): del epochs

        gc.collect() 
        print(f"The temporary memory for {subject_id} has been cleared.")

    print("\n==== Batch processing finished. ====")

else:
    print('Data processing is not permitted.')