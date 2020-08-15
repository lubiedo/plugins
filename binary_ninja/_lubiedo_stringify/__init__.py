# annoyingly simple plugin to convert data at addr to a C-style const string
# useful if combined with keybindings
import binaryninja as bn

def stringify(bv, addr):
    buf = ''
    br  = bn.BinaryReader(bv, bn.Endianness.BigEndian)
    br.seek(addr) # goto addr

    # read data and find null byte
    while True:
        if br.eof: # eof?
            print("Error converting to string: EOF.")
            return

        byte = br.read8() # read byte
        if byte == 0:
            break
        buf += chr(byte) # append to buffer

    # finished, now lets setup a type for it
    type, _ = bv.parse_type_string("char const [%d]" % (len(buf) + 1 )) # count the NULL byte
    bv.define_data_var(addr, type)

bn.PluginCommand.register_for_address("Convert address to null-terminated string",
    "Data in address will be converted to a C-style string", stringify)
