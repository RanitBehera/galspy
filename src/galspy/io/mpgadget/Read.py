import numpy, os,galspec,bigfile
from galspec.IO.Field import _Field
from galspec.IO.Header import _FieldHeader

# decide if bigfile to be used depending on config and
# abstract one read function here instead of Field read function.


def _ReadFieldWithNumpy(field:_Field):
    if not isinstance(field,_Field):raise TypeError
    header = _FieldHeader(field.path + os.sep + "header")

    data=numpy.zeros(header.total_data_length*header.NMEMB,dtype=header.DTYPE)
    for i in range(0,header.NFILE):
        # filename='{:06}'.format(i)
        filename=("{:X}".format(i)).upper().rjust(6,'0')  
        filepath=field.path + os.sep + filename
        with open (filepath, mode='rb') as file:   # b is important -> binary
            fill_start_index = sum(header.datalength_per_file[0:i])   * header.NMEMB
            fill_end_index   = sum(header.datalength_per_file[0:i+1]) * header.NMEMB
            data[fill_start_index:fill_end_index]=numpy.fromfile(file,dtype=header.DTYPE)

    if header.NMEMB>1: data = data.reshape(header.total_data_length,header.NMEMB)

    return data


def _ReadFieldWithBigFile(field:_Field):
    if not isinstance(field,_Field):raise TypeError
    relative_path=str(field.path).split(galspec.CONFIG.MPGADGET_OUTPUT_DIR)[1]
    relative_chunks=relative_path.split("/")
    snap_chunk=relative_chunks[1]
    part_chunk=relative_chunks[2]+os.sep
    field_chunk=relative_chunks[3]

    f=bigfile.File(galspec.CONFIG.MPGADGET_OUTPUT_DIR + os.sep + snap_chunk)
    data = bigfile.Dataset(f[part_chunk],[field_chunk])[:]
    return data

