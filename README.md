# x_data
## some instructions
### github
#### git add.
#### git commit -m ""
#### git push -u origin main 
### django
#### python manage.py runserver
#### python manage.py makemigrations
#### python manage.py migrate
#### python manage.py startapp samples
#### python manage.py shell
#### python manage.py createsuperuser
### django celery
#### export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
#### celery -A x_data worker --loglevel=info
#### celery -A x_data beat --loglevel=info
### st url
#### https://victor-llm-sample.streamlit.app/
###
#### TRUNCATE TABLE stocks_stockhistorybfq, stocks_stockhistoryhfq, stocks_stockhistoryqfq RESTART IDENTITY CASCADE;
### Tips
#### 对于初始化trading_date, 每年年初都需增加当前的数据，以后进行更新分析时应该是以这个时期为锚点的。
#### stocks.management.commands中init_trading_dates有两个，创建这两个文件是在2024年10月30日15时以前，历史数据没有30日
#### 的数据，所以_s1文件标注的是19901219日到20241029的交易日，_s2是20241030至年底的标注。
#### 之所以这么做是因为，根据stockhistoryqfq的历史数据20241029以前有8830个交易日，但如果加上条件，即工作日也算交易日则会多余
#### 8830个，故以历史数据为准，2024年10月30日至年底的数据则根据如果为周末则为非交易日。

