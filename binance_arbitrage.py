from binance.client import Client
import time
from binance.exceptions import BinanceAPIException, BinanceOrderException
import json



#Real
api_key = ""
secret_key = ""


client = Client(api_key, secret_key)
# client.API_URL = 'https://testnet.binance.vision/api'

ticker = client.get_symbol_ticker()

btclist = []
usdtlist = []

for base in ticker:
    if base['symbol'][-4:]=="USDT":
        usdtlist.append(base['symbol'][:-4])
    if base['symbol'][-3:]=="BTC":
        btclist.append(base['symbol'][:-3])
    if base['symbol']=='PAXBTC':
        print("Damn it")
btclist = set(btclist)
usdtlist = set(usdtlist)

common_c = btclist.intersection(usdtlist)
print("Lenght: {}".format(len(common_c)))
trade_cap_in_usdt = 10



counter = 0
display = 0
while 1:
    time.sleep(0)
    try:
        for base in common_c:
            flag1 = 0
            flag2 = 0

            # base = 'AOA'
            
            
            #Collect info
            budict = client.get_orderbook_ticker(symbol='BTCUSDT')
            baseudict = client.get_orderbook_ticker(symbol='{}USDT'.format(base))
            basebdict = client.get_orderbook_ticker(symbol='{}BTC'.format(base))

            #BTC/USDT
            buaskPrice = float(budict['askPrice'])
            bubidPrice = float(budict['bidPrice'])
            buaskQty = float(budict['askQty'])
            bubidQty = float(budict['bidQty'])
            
            #Base/USDT
            baseuaskPrice = float(baseudict['askPrice'])
            baseubidPrice = float(baseudict['bidPrice'])
            baseuaskQty = float(baseudict['askQty'])
            baseubidQty = float(baseudict['bidQty'])

            #Base/BTC
            basebaskPrice = float(basebdict['askPrice'])
            basebbidPrice = float(basebdict['bidPrice'])
            basebaskQty = float(basebdict['askQty'])
            basebbidQty = float(basebdict['bidQty'])



            basename = base



            # #BTC/USDT
            # buaskPrice = 49103.9
            # bubidPrice = 49103.8
            # buaskQty = 0.095489
            # bubidQty = 0.09898436
            
            # #Base/USDT
            # baseuaskPrice = 0.0033049
            # baseubidPrice = 0.0032883
            # baseuaskQty = 116.3247
            # baseubidQty = 806.3784

            # #Base/BTC
            # basebaskPrice = 7e-08
            # basebbidPrice = 6e-08
            # basebaskQty = 5553876.9036
            # basebbidQty = 24529627.3663







            #Ask->Selling
            #Bid->Buying

            
            #USDT -> Base -> BTC -> USDT
            base = trade_cap_in_usdt/baseuaskPrice
            
            BTC = base*basebbidPrice
            
            USDT1 = BTC*bubidPrice

            if display  and USDT1-trade_cap_in_usdt>0:
                print("Base: ",base,baseuaskQty>base)
                print("BTC:",BTC,basebbidQty>base)
                print("USDT1:",USDT1,bubidQty>BTC,"\n\n")

            if baseuaskQty>base and basebbidQty>base and bubidQty>BTC:
                flag1 = 1


            #USDT -> BTC -> Base -> USDT
            BTC = trade_cap_in_usdt/buaskPrice
            
            base = BTC/basebaskPrice
            
            USDT2 = base*baseubidPrice

            if display and USDT2-trade_cap_in_usdt>0:
                print("BTC: ",BTC,buaskQty>BTC)
                print("Base:",base,basebaskQty>base)
                print("USDT2:",USDT2,baseubidQty>base,'\n\n')

            if buaskQty>BTC and basebaskQty>base and baseubidQty>USDT2:
                flag2 = 1

            if display:
                print("\n")
                print("BTC/USDT Informations:")
                print("\tBest Ask Price: {}".format(buaskPrice))
                print("\tBest Ask Size: {}".format(buaskQty))
                print("\tBest Bid Price: {}".format(bubidPrice))
                print("\tBest Bid Size: {}".format(bubidQty))

                print("Base/USDT Informations:")
                print("\tBest Ask Price: {}".format(baseuaskPrice))
                print("\tBest Ask Size: {}".format(baseuaskQty))
                print("\tBest Bid Price: {}".format(baseubidPrice))
                print("\tBest Bid Size: {}".format(baseubidQty))

                print("Base/BTC Informations:")
                print("\tBest Ask Price: {}".format(basebaskPrice))
                print("\tBest Ask Size: {}".format(basebaskQty))
                print("\tBest Bid Price: {}".format(basebbidPrice))
                print("\tBest Bid Size: {}".format(basebbidQty))

                
            flagin = 0
            if USDT1-trade_cap_in_usdt>0.003*trade_cap_in_usdt and flag1:
                flagin = 1
                print("\n")
                print("\tBase: {} Procedure: USDT -> Base -> BTC -> USDT Profit: {} Flag:{}".format(basename,USDT1-trade_cap_in_usdt,flag1))

            if USDT2-trade_cap_in_usdt>0.003*trade_cap_in_usdt and flag2:
                flagin = 1
                print("\n")
                print("\tBase: {} Procedure: USDT -> BTC -> Base -> USDT Profit: {} Flag:{}".format(basename,USDT2-trade_cap_in_usdt,flag2))

            # if USDT1-trade_cap_in_usdt>0.00*trade_cap_in_usdt:
            #     flagin = 1
            #     print("\n")
            #     print("Base: {} Procedure: USDT -> Base -> BTC -> USDT Profit: {} Flag:{}".format(basename,USDT1-trade_cap_in_usdt,flag1))
            #     # exit(0)

            # if USDT2-trade_cap_in_usdt>0.00*trade_cap_in_usdt:
            #     flagin = 1
            #     print("\n")
            #     print("Base: {} Procedure: USDT -> BTC -> Base -> USDT Profit: {} Flag:{}".format(basename,USDT2-trade_cap_in_usdt,flag2))  
            #     # exit(0)

            if flagin and (flag1 or flag2):
                print("\n")
                print(flag1,flag2)
                print("BTC/USDT Informations:")
                print("\tBest Ask Price: {}".format(buaskPrice))
                print("\tBest Ask Size: {}".format(buaskQty))
                print("\tBest Bid Price: {}".format(bubidPrice))
                print("\tBest Bid Size: {}".format(bubidQty))

                print("Base/USDT Informations:")
                print("\tBest Ask Price: {}".format(baseuaskPrice))
                print("\tBest Ask Size: {}".format(baseuaskQty))
                print("\tBest Bid Price: {}".format(baseubidPrice))
                print("\tBest Bid Size: {}".format(baseubidQty))

                print("Base/BTC Informations:")
                print("\tBest Ask Price: {}".format(basebaskPrice))
                print("\tBest Ask Size: {}".format(basebaskQty))
                print("\tBest Bid Price: {}".format(basebbidPrice))
                print("\tBest Bid Size: {}".format(basebbidQty))


            counter+=1
            print("\r{}:{}            ".format(counter,basename),end='')
            
    except Exception as e:
        if e==KeyboardInterrupt:
            break
        
        # print(basename)
        # print("\n")
        # print("BTC/USDT Informations:")
        # print("\tBest Ask Price: {}".format(buaskPrice))
        # print("\tBest Ask Size: {}".format(buaskQty))
        # print("\tBest Bid Price: {}".format(bubidPrice))
        # print("\tBest Bid Size: {}".format(bubidQty))

        # print("Base/USDT Informations:")
        # print("\tBest Ask Price: {}".format(baseuaskPrice))
        # print("\tBest Ask Size: {}".format(baseuaskQty))
        # print("\tBest Bid Price: {}".format(baseubidPrice))
        # print("\tBest Bid Size: {}".format(baseubidQty))

        # print("Base/BTC Informations:")
        # print("\tBest Ask Price: {}".format(basebaskPrice))
        # print("\tBest Ask Size: {}".format(basebaskQty))
        # print("\tBest Bid Price: {}".format(basebbidPrice))
        # print("\tBest Bid Size: {}".format(basebbidQty))
        # break
        print("\rFozen.",end='')



print("\n")
