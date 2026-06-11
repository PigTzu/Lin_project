# Multi-timescale Neural Dynamics for Multisensory Integration in Autism Spectrum Condition
This is an ongoing project for Brainhack School 2026, which I try to do time-frequency analysis using MNE-python. Dataset from [OpenNeuro ds006777](https://openneuro.org/datasets/ds006777/versions/1.0.0) would be used, and the entire processing/analyzing workflow and scripts will be updated.
## Background
- Our responses to multisensory stimuli typically differ from the combined responses of the corresponding unisensory stimuli. We have supra-additive responses which means the effect of multisensory integration is larger than combined unimodal responses; the other one is sub-additive responses, meaning that the effect of multisensory integration is smaller than the combined unimodal effects.
- Larger alpha suppression serves as a marker for increased integration of information, indexing heightened integration load. This multisensory integration (MSI) effect went beyond a mere summation of unimodal power responses alone[^1].
- Different timescales, reflected in different oscillatory frequency bands, serve to route different information types through cortical networks[^2].
- Individuals with autism spectrum condition (ASC) has altered MSI time window; however few studies investigated MSI on this population through a multi-timescale approach.
## Research Aims
- Comparing the MSI effects (measured with alpha suppression) between ASC and TD groups.
- Exploring the MSI effects across different frequency bands spatially and temporally.
## Dataset Description
- The dataset was downloaded from OpenNeuro ds006777[^3]. It is an EEG dataset collected by BioSemi system, and I would include TD and ASC participants in my analyses.
- Participants did an audiovisual simple reaction-time task (AVSRT). The stimulus type consisted of visual stimulus alone, auditory stimulus alone, and combined audiovisual stimuli simultaneously. What participants should do was press the button as quickly as possible when they detected any stimulus.
## Data Analyses
Preprocessing and time-frequency would be done through MNE-python 1.12.1 with libraries [PyPREP](https://pyprep.readthedocs.io/en/stable/index.html)[^7] to detect noisy channels and [autoreject](https://autoreject.github.io/stable/index.html)[^8] to reject bad epochs automatically. Specific processes would refer to Vanneau et al. (2025)[^4], Matyjek et al. (2025)[^5], and Gao et al. (2021)[^6].

So far preprocessing scripts have been uploaded but still need time to modify.
## Something I Want to Discuss
- Preprocessing steps are different between three studies investigating multisensory integration[^4][^5][^6], and I think some steps used in the [script](https://github.com/tvanneau/Cross-sensory-switching/blob/main/Preprocessing_AVSRT_Project.py) by Vanneau et al. (2025) would generate controversial issues. Hope to discuss this orally.
- The number of participants in the two groups (TD vs. ASC) is different. How can I make sure SNR between groups are the same?
[^1]: Matyjek, M., Kita, S., Torralba Cuello, M., & Soto Faraco, S. (2024). Multisensory integration of speech and gestures in a naturalistic paradigm. Human brain mapping, 45(11), e26797.
[^2]: Senkowski, D., & Engel, A. K. (2024). Multi-timescale neural dynamics for multisensory integration. Nature Reviews Neuroscience, 25(9), 625-642.
[^3]: Theo Vanneau, John J. Foxe, Shlomit Beker, Daniella Cohen, Albulena Sejdu, and Sophie Molholm (2025). SFARI AVSRT EEG. OpenNeuro. [Dataset] doi: doi:10.18112/openneuro.ds006777.v1.0.0
[^4]: Vanneau, T., Foxe, J. J., Beker, S., & Molholm, S. (2025). Disrupted Top-Down Modulation as a Mechanism of Impaired Multisensory Processing in Children with an Autism Spectrum Diagnosis. bioRxiv, 2025-11.
[^5]: Matyjek, M., Kita, S., Cuello, M.T., & Faraco, S.S. (2025), Multisensory Integration of Naturalistic Speech and Gestures in Autistic Adults. Autism Research, 18: 1156-1169.
[^6]: Gao, C., Xie, W., Green, J. J., Wedell, D. H., Jia, X., Guo, C., & Shinkareva, S. V. (2021). Evoked and induced power oscillations linked to audiovisual integration of affect. Biological psychology, 158, 108006.
[^7]: Bigdely-Shamlo, N., Mullen, T., Kothe, C., Su, K. M., & Robbins, K. A. (2015). The PREP pipeline: standardized preprocessing for large-scale EEG analysis. Frontiers in neuroinformatics, 9, 16.
[^8]: Jas, M., Engemann, D. A., Bekhti, Y., Raimondo, F., & Gramfort, A. (2017). Autoreject: Automated artifact rejection for MEG and EEG data. NeuroImage, 159, 417-429.
