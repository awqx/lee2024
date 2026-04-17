import numpy as np
import pandas as pd

import warnings

from dataclasses import dataclass
from typing      import List, Union

from ..registry import registry


@registry.register
@dataclass
class SpikeAverages:
    """Stores averaged neural responses indexed by some grouping."""
    # Dictionary mapping 'family_name' -> np.ndarray [spikes x Channels]
    avgs: dict[str, np.ndarray]
    area: str
    subj: Union[str, List[str]]
    grouping: str
    
    def get_group(self, name: str):
        return self.avgs.get(name)


@registry.register
def avg_by_stim(
    session, 
    stim_col: Union[str, int], 
    over_neurons: bool
) -> 'SpikeAverages':
    """
    Groups neural 'spikes' by a named or index column in session.stim 
    and returns a SpikeAverages object.

    Parameters
    ----------
    session: RecordingSessions
        spiking data to average over
    
    stim_col: Union[str, int]
        either name or index of column in `stim` to do grouping over

    over_neurons: bool, optional
        whether to also average over neurons, default=True
    """

    if isinstance(stim_col, int):
        grps = session.stim[:, stim_col]
    else: 
        grps = session.stim[stim_col] 
    grps = grps.to_numpy()
    unique_grps = np.unique(grps)

    if len(unique_grps) > len(grps) // 2: 
        warnings.warn(
            "Number of unique groups exceeds half of total rows", UserWarning)

    grps_avgs = {}
    
    for i in unique_grps:
        indices = np.where(grps == i)[0]
        family_data = session.spikes[indices, :, :]
        
        if over_neurons: 
            # average across samples and neurons (axes [0, 2])
            grps_avgs[str(i)] = np.mean(family_data, axis=(0, 2))
        else: 
            # average across the samples (axis 0): [spikes x Channels]
            grps_avgs[str(i)] = np.mean(family_data, axis=0) 
        
    return SpikeAverages(
        avgs=grps_avgs,
        area=session.area,
        subj=session.subj,
        grouping="coherence",
    )

@registry.register
def avg_sessions(
    sessions: dict, 
    stim_col: Union[str, int], 
    over_neurons: bool = False
) -> dict: 
    """
    Wrapper for applying `avg_by_stim` over a dictionary of 
    `RecordingSession` instances

    Parameters
    ----------
    sessions: dict
        dictionary of RecordingSessions, such as the one produced by 
        `load_matlab_dir`
    
    stim_col: Union[str, int]
        either name or index of column in `stim` to do grouping over

    over_neurons: bool, optional
        whether to also average over neurons, default=True
    """
    sessions_avgs = {}
    # TODO: shorten this with list comprehension
    for k, sesh in sessions.items(): 
        sessions_avgs[k] = avg_by_stim(sesh, stim_col, over_neurons)
    
    return sessions_avgs 
 