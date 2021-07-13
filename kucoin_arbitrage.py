import threading
from kucoin.client import Client
import time

api_key = ''
api_secret = ''
api_passphrase = ''
client = Client(api_key, api_secret, api_passphrase)


symbols = client.get_symbols()
btcpairskucoin = set([x['symbol'].split('-')[0] for x in symbols if x['quoteCurrency']=='BTC'])
usdtpairskucoin = set([x['baseCurrency'].split('-')[0] for x in symbols if x['quoteCurrency']=='USDT'])
common_c = btcpairskucoin.intersection(usdtpairskucoin)

trade_cap_in_usdt = 100


while 1:
    time.sleep(0)
    try:
        for base in common_c:
            flag1 = 0
            flag2 = 0

            # base = 'AOA'
            print("\r{}        ".format(base),end='')
            
            #Collect info
            budict = client.get_ticker('BTC-USDT')
            baseudict = client.get_ticker('{}-USDT'.format(base))
            basebdict = client.get_ticker('{}-BTC'.format(base))

            #BTC/USDT
            bubestAsk = float(budict['bestAsk'])
            bubestBid = float(budict['bestBid'])
            bubestAskSize = float(budict['bestAskSize'])
            bubestBidSize = float(budict['bestBidSize'])
            
            #Base/USDT
            baseubestAsk = float(baseudict['bestAsk'])
            baseubestBid = float(baseudict['bestBid'])
            baseubestAskSize = float(baseudict['bestAskSize'])
            baseubestBidSize = float(baseudict['bestBidSize'])

            #Base/BTC
            basebbestAsk = float(basebdict['bestAsk'])
            basebbestBid = float(basebdict['bestBid'])
            basebbestAskSize = float(basebdict['bestAskSize'])
            basebbestBidSize = float(basebdict['bestBidSize'])







            # #BTC/USDT
            # bubestAsk = 49103.9
            # bubestBid = 49103.8
            # bubestAskSize = 0.095489
            # bubestBidSize = 0.09898436
            
            # #Base/USDT
            # baseubestAsk = 0.0033049
            # baseubestBid = 0.0032883
            # baseubestAskSize = 116.3247
            # baseubestBidSize = 806.3784

            # #Base/BTC
            # basebbestAsk = 7e-08
            # basebbestBid = 6e-08
            # basebbestAskSize = 5553876.9036
            # basebbestBidSize = 24529627.3663







            #Ask->Selling
            #Bid->Buying

            #USDT -> Base -> BTC -> USDT
            base = trade_cap_in_usdt/baseubestAsk
            # print("Base: ",base,baseubestAskSize>base)
            BTC = base*basebbestBid
            # print("BTC:",BTC,basebbestBidSize>base)
            USDT1 = BTC*bubestBid
            # print("USDT1:",USDT1,bubestBidSize>BTC,"\n\n")

            if baseubestAskSize>base and basebbestBidSize>base and bubestBidSize>BTC:
                flag1 = 1


            #USDT -> BTC -> Base -> USDT
            BTC = trade_cap_in_usdt/bubestAsk
            # print("BTC: ",BTC,bubestAskSize>BTC)
            base = BTC/basebbestAsk
            # print("Base:",base,basebbestAskSize>base)
            USDT2 = base*baseubestBid
            # print("USDT2:",USDT2,baseubestBidSize>base,'\n\n')

            if bubestAskSize>BTC and basebbestAskSize>base and baseubestBidSize>USDT2:
                flag2 = 1

            # if 1:
            #     print("\n")
            #     print("BTC/USDT Informations:")
            #     print("\tBest Ask Price: {}".format(bubestAsk))
            #     print("\tBest Ask Size: {}".format(bubestAskSize))
            #     print("\tBest Bid Price: {}".format(bubestBid))
            #     print("\tBest Bid Size: {}".format(bubestBidSize))

            #     print("Base/USDT Informations:")
            #     print("\tBest Ask Price: {}".format(baseubestAsk))
            #     print("\tBest Ask Size: {}".format(baseubestAskSize))
            #     print("\tBest Bid Price: {}".format(baseubestBid))
            #     print("\tBest Bid Size: {}".format(baseubestBidSize))

            #     print("Base/BTC Informations:")
            #     print("\tBest Ask Price: {}".format(basebbestAsk))
            #     print("\tBest Ask Size: {}".format(basebbestAskSize))
            #     print("\tBest Bid Price: {}".format(basebbestBid))
            #     print("\tBest Bid Size: {}".format(basebbestBidSize))

            

            if USDT1-trade_cap_in_usdt>0.003*trade_cap_in_usdt and flag1:
                print("\n")
                print("\tBase: {} Procedure: USDT -> Base -> BTC -> USDT Profit: {} Flag:{}".format(base,USDT1-trade_cap_in_usdt,flag1))

            if USDT2-trade_cap_in_usdt>0.003*trade_cap_in_usdt and flag2:
                print("\n")
                print("\tBase: {} Procedure: USDT -> BTC -> Base -> USDT Profit: {} Flag:{}".format(base,USDT2-trade_cap_in_usdt,flag2))

            if USDT1-trade_cap_in_usdt>0.003*trade_cap_in_usdt:
                print("\n")
                print("Base: {} Procedure: USDT -> Base -> BTC -> USDT Profit: {} Flag:{}".format(base,USDT1-trade_cap_in_usdt,flag1))

            if USDT2-trade_cap_in_usdt>0.003*trade_cap_in_usdt:
                print("\n")
                print("Base: {} Procedure: USDT -> BTC -> Base -> USDT Profit: {} Flag:{}".format(base,USDT2-trade_cap_in_usdt,flag2))  
    except:
        print("\rQuota Exceeded.",end='')


print("\n")
