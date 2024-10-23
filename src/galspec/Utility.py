import numpy


def ContinnumFinder(ang,flam,ang_start:int,ang_end:int):
    cxdata=[]
    cydata=[]

    span= AVERAGING_SPAN
    for i in range(span,len(xdata)-span):
        if xdata[i]<1250 or xdata[i]>1900 : continue
        if True:
            if (xdata[i]>1520 and xdata[i]<1570) :continue

        chunk=ydata[i-span:i+span+1]
        chunk_avg=numpy.average(chunk)
        rel_offset = chunk-chunk_avg

        sumy = numpy.sum(chunk*numpy.exp(-rel_offset**2/0.01))
        sumy/= numpy.sum(numpy.exp(-rel_offset**2/0.01))

        # sumy = numpy.sum(chunk*numpy.exp(rel_offset/0.01))
        # sumy/= numpy.sum(numpy.exp(rel_offset/0.01))

        cydata.append(sumy)
        cxdata.append(xdata[i])
    
    cxdata = numpy.array(cxdata)
    cydata = numpy.array(cydata)

def SlopeFinder(ang,flam,ang_start:int,ang_end:int):
    
    pass