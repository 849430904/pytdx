# coding=utf-8

import os
import sys
import click

from collections import OrderedDict
import pprint

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams


api = TdxHq_API()


def get_security_quotes(params):
    market, code = params
    stocks = api.get_security_quotes([(int(market), code),])
    return (stocks)

def get_security_bars(params):
    category, market, code, start, count = params
    return (api.get_security_bars(int(category), int(market), code, int(start), int(count)))

def get_security_count(params):
    return (api.get_security_count(int(params[0])))

def get_security_list(params):
    return (api.get_security_list(int(params[0]), int(params[1])))

def get_index_bars(params):
    category, market, code, start, count = params
    return (api.get_index_bars(int(category), int(market), code, int(start), int(count)))

def get_minute_time_data(params):
    return (api.get_minute_time_data(int(params[0]), params[1]))

def get_history_minute_time_data(params):
    return (api.get_history_minute_time_data(int(params[0]), params[1], int(params[2])))

def get_transaction_data(params):
    return (api.get_transaction_data(int(params[0]), params[1], int(params[2]), int(params[3])))

def get_history_transaction_data(params):
    return (api.get_history_transaction_data(int(params[0]), params[1], int(params[2]), int(params[3]), int(params[4])))

def get_company_info_category(params):
    return (api.get_company_info_category(int(params[0]), params[1]))

def get_company_info_content(params):
    return (api.get_company_info_content(int(params[0]), params[1], params[2], int(params[3]), int(params[4])))

def get_xdxr_info(params):
    return (api.get_xdxr_info(int(params[0]), params[1]))

def get_finance_info(params):
    return (api.get_finance_info(int(params[0]), params[1]))

FUNCTION_LIST = OrderedDict(
    [
        (1, ['获取股票行情', '参数：市场代码， 股票代码， 如： 0,000001 或 1,600300', get_security_quotes, '0,000001']),
        (2, ['获取k线', '''category-> K线种类
0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
5 周K线
6 月K线
7 1分钟
8 1分钟K线 9 日K线
10 季K线
11 年K线
market -> 市场代码 0:深圳，1:上海
stockcode -> 证券代码;
start -> 指定的范围开始位置;
count -> 用户要请求的 K 线数目，最大值为 800

如： 9,0,000001,0,100''', get_security_bars, '9,0,000001,0,100']),
        (3, ['获取市场股票数量', '参数：市场代码， 股票代码， 如： 0 或 1', get_security_count, '0']),
        (4, ['获取股票列表', '参数：市场代码, 起始位置， 数量  如： 0,0 或 1,100', get_security_list, '0,0']),
        (5, ['获取指数k线', """参数:
category-> K线种类
0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线
5 周K线
6 月K线
7 1分钟
8 1分钟K线 9 日K线
10 季K线
11 年K线
market -> 市场代码 0:深圳，1:上海
stockCode -> 证券代码;
start -> 指定的范围开始位置; count -> 用户要请求的 K 线数目
如：9,1,000001,0,100""", get_index_bars, '9,1,000001,0,100']),
        (6, ['查询分时行情', "参数：市场代码， 股票代码， 如： 0,000001 或 1,600300", get_minute_time_data, '0,000001']),
        (7, ['查询历史分时行情', '参数：市场代码， 股票代码，时间 如： 0,000001,20161209 或 1,600300,20161209', get_history_minute_time_data, '0,000001,20161209']),
        (8, ['查询分笔成交', '参数：市场代码， 股票代码，起始位置， 数量 如： 0,000001,0,10', get_transaction_data, '0,000001,0,10']),
        (9, ['查询历史分笔成交', '参数：市场代码， 股票代码，起始位置，日期 数量 如： 0,000001,0,10,20170209', get_history_transaction_data, '0,000001,0,10,20170209']),
        (10, ['查询公司信息目录','参数：市场代码， 股票代码， 如： 0,000001 或 1,600300', get_company_info_category, '0,000001']),
        (11, ['读取公司信息详情', '参数：市场代码， 股票代码, 文件名, 起始位置， 数量, 如：0,000001,000001.txt,2054363,9221', get_company_info_content, '0,000001,000001.txt,2054363,9221']),
        (12, ['读取除权除息信息', '参数：市场代码， 股票代码， 如： 0,000001 或 1,600300', get_xdxr_info, '0,000001']),
        (13, ['读取财务信息', '参数：市场代码， 股票代码， 如： 0,000001 或 1,600300', get_finance_info, '0,000001']),
    ]
)

def connect():
    c = api.connect('101.227.73.20', 7709)
    if not c:
        raise Exception("无法连接")

def disconnect():
    api.disconnect()


@click.command()
@click.option('-f', '--function', default=0, type=click.INT, help="选择使用的功能")
@click.option('--df/--no-df', default=True, help="是否使用Pandas Dataframe显示")
def main(function, df):
    click.secho("连接中.... ", fg="green")
    connect()
    click.secho("连接成功！", fg="green")
    if function == 0:

        while True:
            click.secho("-" * 20)
            click.secho("功能列表：")
            for (k,v) in FUNCTION_LIST.items():
                click.secho(str(k) + " : " + v[0], bold=True)
                last = k + 1
            click.secho(str(last) + " : 退出断开连接", bold=True)
            click.secho("-" * 20)
            value = click.prompt('请输入要使用的功能', type=int)
            if value == last:
                break
            click.secho("你选择的是功能 " + str(value) + " : " + FUNCTION_LIST[value][0])
            click.secho("-" * 20)

            click.secho(FUNCTION_LIST[value][1])
            params_str = click.prompt("请输入参数 ", type=str, default=FUNCTION_LIST[value][3])
            params = [p.strip() for p in params_str.split(",")]
            click.secho("-" * 20)
            try:
                result = FUNCTION_LIST[value][2](params)
                if df:
                    result = api.to_df(result)
                    print(result)
                else:
                    pprint.pprint(result)
            except Exception as e:
                click.secho("发生错误，错误信息为： " + str(e), fg='red')

            click.secho("-" * 20)
            click.echo("按任意键继续")
            click.getchar()


    elif function == 1:
        pass

    click.secho("断开连接中.... ", fg="green")
    disconnect()
    click.secho("断开连接成功！", fg="green")



if __name__ == '__main__':
    main()