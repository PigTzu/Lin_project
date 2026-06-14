from pyprep.find_noisy_channels import NoisyChannels

def mark_bad_channels(raw):
    raw = raw.copy()
    raw.filter(l_freq=1.0, h_freq=45.0)
    nd = NoisyChannels(raw)
    nd.find_all_bads(ransac=True, channel_wise=True) # Call all the functions to detect bad channels.
    bads = nd.get_bads() # Get the names of all channels currently flagged as bad. Returns bads
    return bads # list or dict of bad channels