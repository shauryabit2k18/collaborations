import matplotlib.pyplot as plt
import json
# import Image
a = [ '{ "f" : "True" }', '{ "f" : "True"}' , '{ "a" : "True" }' , '{ "b" : "True" }', '{"c" : "False"}']
f = []
def fplot():
    for i in a:
        # print(i)
        data = json.loads(str(i))
        frequency = data["frequency"]
        print(frequency)
        f.append(frequency)

    plt.plot(f)
    plt.savefig("fplot.jpg")
    plt.ylabel('frequency')
    plt.show()

def piechart(a):
    freq = {}
    labels = []
    values = []
    for i in a:
        data = json.loads(str(i))
        for d in data:
            print(type(d))
            print()
            if (d in freq) and (data[d]=='True') :
                freq[d]+=1
            elif (data[d]=='True'):
                freq[d] = 1    
    for j in freq:
        labels.append(str(j))
        values.append(freq[j])

    figureObject, axesObject = plt.subplots()
    axesObject.pie(values, autopct='%1.2f',startangle=90, shadow = True)     
    #TODO : Enter relative path location
    plt.savefig("pplot.jpg")
    plt.legend(labels)
    plt.show()   

def sendFile(str):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='plot')

    channel.basic_publish(exchange='', routing_key='plot', body=msg)
    connection.close()

