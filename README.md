# The classification of volcan signals（single station）

THe spatiotemporal evolutions of long-period(LP), hybrid and volcanic tectonic (VT) seismicity are important for tracking the evolution of underlying volcanic proces. Here, by defining a spectral dissimilarity metric, we perform cluster analysis in seismic events in Kilauea volcano.


## data
The data are HV.OTLD, From Jan., 2011 to Oct., 2018．The window length of each event is 10s before the p wave arrival time and 10s after S wave arriival time
> The length can be shorter than this example, but sholud be more than 5 sec. The name of the events is the original time of eathquakes (The catalog time).

## config_json
"data_dir": The path of sac files.
"snr": 3
"win_len": 1.28 (We select the 12.8s before and after P wave arrival time to calculate the spectrum)
"events_catalog": "events_catalog" (events catalog)
"n_cls": 20 (The number of clusters)

## Run the script
You can run the test code as:
```
python volcano_signals_classification.py (-P) config_json
```
## Results
`out\png` : clsi.pdf (100 spectra of each clusters); mean_spectra; fre_energy;  med_dis.pdf; hist.png and dendrogram.pdf
`out\text`: clusteri.dat (the catalog of 20 clusters); new_catalog (add FI and cluster Num. to the events_catalog)
peak_amp_size: used to plot fre_energy.pdf

```

