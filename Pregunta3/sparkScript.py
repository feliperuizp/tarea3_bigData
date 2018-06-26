from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.flume import FlumeUtils
import uuid
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: flume_wordcount.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)
    uid = str(uuid.uuid4())
    sc = SparkContext(appName="PythonStreamingFlumeWordCount")
    ssc = StreamingContext(sc, 1)

    hostname, port = sys.argv[1:]
    kvs = FlumeUtils.createStream(ssc, hostname, int(port))
    lines = kvs.map(lambda x: x[1])
    counts = lines.filter(lambda line: "sales" in line.lower())\
		  .map(lambda word: (uid, word)) \
                  .reduceByKey(lambda a, b: a+b) \
		  .saveAsTextFiles('hdfs://0.0.0.0:8020/weblogs/sales_','txt')
		  

    ssc.start()
    ssc.awaitTermination()
