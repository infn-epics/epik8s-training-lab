from org.csstudio.display.builder.runtime.script import PVUtil

class Serializer:
    _pv = None
    _arr_double = None
    _custom_pv_name = None

    def __init__(self, pv_data, custom_pv_name=None):
        self._pv = pv_data
        self._arr_double = PVUtil.getDoubleArray(pv_data)
        self._custom_pv_name = custom_pv_name
    
    def _add_pvname(self):
        if (self._custom_pv_name != None):
            pv_name = self._custom_pv_name
        else:
            pv_name = self._pv.getName()
        
        return "PV[LEN: " + str(len(pv_name)) + "]: " + pv_name + "; "
        
    def _add_timestamp(self):
        pv_ts = PVUtil.getTimeString(self._pv)
        
        return "TS: " + pv_ts + "; "
    
    def _add_data(self):
        data_info = "DATA: "

        # This would be easier with split(), but it doesn't work with _arr_double
        nelem = len(self._arr_double)
        for i in range(0, nelem):
            data_info += str(self._arr_double[i])
            if (i < (nelem - 1)):
                data_info += "; "

        data_info += "\n"
        
        return data_info
    
    def serialize(self):
        s = self._add_pvname()
        s += self._add_timestamp()
        s += self._add_data()
    
        return s


class Deserializer:
    _data = None

    def __init__(self, serialized_data):
        # Remove any leading/trailing newlines
        self._data = serialized_data.strip()
    
    def _parse_pvname(self, pv):
        # Markers for finding PV length and name
        LEN_START = "LEN:"
        LEN_END = "]"
        NAME_START = "]:"
        
        # Get length of PV name
        pv_name_len = pv[pv.find(LEN_START) + len(LEN_START) : pv.find(LEN_END)].strip()
        pv_name_len = int(pv_name_len)
        
        # Get PV name
        pv_name = pv[(pv.find(NAME_START) + len(NAME_START)):].strip()
        pv_name = pv_name[:pv_name_len]
        
        return pv_name
        
    def _parse_timestamp(self, pv):
        # Markers for finding PV timestamp
        TS_START = "TS:"
        TS_DELIM = "; "
        
        #TODO: skip over name part
        pv_ts = pv[pv.find(TS_START) + len(TS_START):].strip()
        pv_ts = pv_ts[:pv_ts.find(TS_DELIM)]
        
        return pv_ts

    def _parse_pvdata(self, pv):
        ELEM_START = "DATA:"
        ELEM_DELIM = "; "
        
        elems = pv[pv.find(ELEM_START) + len(ELEM_START):].strip()
        
        # Split elements string into list by element delimitor
        elems = elems.split(ELEM_DELIM)
        
        # Convert elements from string to float
        elems = map((lambda x: float(x)), elems)
        
        return elems
    
    def deserialize(self):
        pvs_deserialized = []
        
        # Format of each line: "PV[LEN: pvname_length]: pvname; DATA: e1; e2; ...; elast"
        # Example: PV[LEN: 14]: loc://some_arr; DATA: 3.0; 1.0; 4.0; 1.0; 9.0; 5.0
        for line in self._data.split("\n"):
            # Try to parse each line, throw exception if anything goes wrong
            try:
                pv_name = self._parse_pvname(line)
                pv_ts = self._parse_timestamp(line)
                pv_data = self._parse_pvdata(line)
            except Exception as e:
                raise Exception("error '"+str(e)+"' parsing :'"+line+"'")
            
            pv = {
                'name':pv_name, 
                'ts':pv_ts, 
                'data':pv_data
                  }
            pvs_deserialized.append(pv)
            
        return pvs_deserialized
