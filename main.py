from binance.client import Client
import datetime
import cryptocompare
import csv

api_key = "EoY3LVBR1lPic8kjbKVnLw1RGOsviNeV2s5hTo7PrRCeMXJDg4l30qhULYiegQCl"
api_secret_key = "PZFiRqnuVIlFBkrAomEriGBeDMCfUgV4tYjGuXuZSzcK04c22ndxSBfKm4uWbVp6"
client = Client(api_key, api_secret_key)

withdraws = client.get_withdraw_history()
deposit = client.get_deposit_history()




asset = 'asset'
amount = 'amount'
txld = 'txId'
depositdate = 'insertTime'
withdrawdate = 'applyTime'
valueAtTheTime = 'Value of Crypto'

# used to keep track of all trading pairs

# get crypto deposite history
def traderDepositHistroy():
    with open("CryptoTrader Deposit History.csv", "w") as csvfile:
        fieldnames = ['asset', 'amount', 'txId', 'insertTime', 'Value of Crypto' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        count = 0
        while (count < len(deposit['depositList'])):

            #convert unix time
            convertedUnixDate = timeStampConverter(deposit['depositList'][count][depositdate])

            # get value of crypto deposit for that day
            value = getPriceThatDay(deposit['depositList'][count][asset], 'USD', timeStampConverter(deposit['depositList'][count][depositdate]))*deposit['depositList'][count][amount]

            # write data to the csv file
            writer.writerow({asset: deposit['depositList'][count][asset],
                             amount: deposit['depositList'][count][amount],
                             txld: deposit['depositList'][count][txld],
                             depositdate: convertedUnixDate,
                             valueAtTheTime: value
                             })
            count = count + 1

# get crypto withdraw history
def traderWithdrawHistroy():
    with open("CryptoTrader Withdraw History.csv", "w") as csvfile:
        fieldnames = ['asset', 'amount', 'txId', 'applyTime', 'Value of Crypto', ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        count = 0
        while (count < len(withdraws['withdrawList'])):
            # convert unix time
            convertedUnixDate = timeStampConverter(withdraws['withdrawList'][count][withdrawdate])

            # get value of crypto deposit for that day
            value = getPriceThatDay(withdraws['withdrawList'][count][asset], 'USD',
                                    timeStampConverter(withdraws['withdrawList'][count][withdrawdate])) * \
                    withdraws['withdrawList'][count][amount]

            # write data to the csv file
            writer.writerow({asset: withdraws['withdrawList'][count][asset],
                             amount: withdraws['withdrawList'][count][amount],
                             txld: withdraws['withdrawList'][count][txld],
                             withdrawdate: convertedUnixDate,
                             valueAtTheTime: value
                             })
            count = count + 1

# convert time stamp to date
def timeStampConverter(unixTime):

    time = int(unixTime)/1000
    newTime  =   datetime.datetime.utcfromtimestamp(time)
    return newTime

# get price of crypto for a giving day
def getPriceThatDay(crytoName, currencyName, timeStamp):
    price = cryptocompare.get_historical_price(crytoName, currencyName, timeStamp)
    return price[crytoName][currencyName]

#get crypto balance
def getCryptoBalance():
    temp = []
    info = client.get_account()
    for key in info['balances']:
        if float(key['free']) > 0.0001:
            temp.append(key)
        else:
            pass

    return temp




# time to get some trades
def getSymbols():
    info = client.get_exchange_info()
    tradeSymbols =  open("CryptoTrader Trading Pairs.txt", "w")
    for i in info['symbols']:
        tradeSymbols.write(i['symbol'])
        tradeSymbols.write('\n')
    tradeSymbols.close()

# get trades base on symbols



