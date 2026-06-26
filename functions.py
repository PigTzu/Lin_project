import os
import mne
import gc
from pyprep.find_noisy_channels import NoisyChannels

def mark_bad_channels(raw):
    raw = raw.copy()
    raw.filter(l_freq=1.0, h_freq=45.0)
    nd = NoisyChannels(raw)
    nd.find_all_bads(ransac=True, channel_wise=True) # Call all the functions to detect bad channels.
    bads = nd.get_bads() # Get the names of all channels currently flagged as bad. Returns bads
    return bads # list or dict of bad channels


def compute_grand_tfr(derivatives_dir,subject_ids,freqs,n_cycles,condition,picks):
    all_power = []

    for subject_id in subject_ids:
            
        epochs_path = os.path.join(derivatives_dir, subject_id, f'{subject_id}_eeg-epo.fif')
        
        try:
            epochs = mne.read_epochs(epochs_path, preload=True) 
            
            power = epochs[condition].compute_tfr(
                method="morlet", 
                freqs=freqs, 
                n_cycles=n_cycles, 
                average=True, 
                decim=4,
                picks=picks
            )
            
            power_file_path = os.path.join(derivatives_dir, subject_id, f'{subject_id}_cond-{condition}_eeg-tfr.h5')
            power.save(power_file_path, overwrite=True)
            
            all_power.append(power)
            
        except Exception as e:
            print(f"{subject_id} failed to be processed: {e}")
            
        finally:
            if 'epochs' in locals(): del epochs
            gc.collect()

    grand_power = mne.grand_average(all_power)

    return grand_power, all_power