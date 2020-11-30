#火山信号分类（单台站）
火山区域长期存在多种信号，包括低频（LP和hybrid）以及高频(普通构造事件和火山构造事件（VT）)．在之前Frequency Index(FI)中，事件呈双峰分布．这里简略介绍一下我们所使用的方法:


## data
数据来自HV.OTLD台站从2011年１月到2018年10月(包括2018年1月到2018年４月模板匹配找到的事件)记录到的事件．每一个事件的波形窗口开始于P波到时10秒之前以及S波到时10秒之后，　并且已经经过了一系列数据预处理过程(去均值, 去仪器响应，去线性趋势等)．
> 数据时间窗口长度可以变化，但是至少要包括P波到时前后各５秒的波形．

## pwave_spectra.py

如果sac文件储存在 `/data/station_name/` 下，不需要任何更改．这个脚本会选出符合要求的（snr>3）事件并截取p波到时前后各1.28s的波形并计算其幅度谱．
输出文件包括：`/output/pkl/amp_container.pkl /output/pkl/TimeSeries_container.pkl　　/output/pkl/name_container.pkl　　　/output/pkl/fi_container.pkl`分别为事件对应的幅度谱，时间序列，事件sac名称，以及计算得到的事件的FI值． 以及所有事件的FI 分布图．


