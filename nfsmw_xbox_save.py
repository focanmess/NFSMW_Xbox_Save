################################################################################
# Need for Speed: Most Wanted Xbox Save Game Editor / Fixer                    #
# Author: Jason                                                                #
################################################################################

from __future__ import print_function
import hashlib
import hmac
import codecs
import struct
import argparse
import sys

# Retail XBE Key
hexXBEKey    = '5C0733AE0401F7E8BA7993FDCD2F1FE0'
# NFSMW Signature Key
hexSigKey    = 'B6B7FC82720BE67A4926DBDA0F1F0807'
# Save Game File Size
sizeSaveGame = 62728
# Tool Description
toolDesc     = 'Need for Speed: Most Wanted Xbox Save Game Editor / Fixer'

hex_decode = codecs.getdecoder('hex_codec')
hex_encode = codecs.getencoder('hex_codec')
if sys.version_info[0] >= 3:
  def bytearray_hexstr(arr):
    return str(hex_encode(arr)[0], 'ascii')
else:
  def bytearray_hexstr(arr):
    return str(hex_encode(arr)[0])

# Main execution
def main():
  # Handle arguments
  parser = argparse.ArgumentParser(description = toolDesc)
  parser.add_argument('savegame', metavar = 'SAVEGAME', help = 'NFSMW Xbox save game file to edit or fix')
  parser.add_argument('-o', '--output', action = 'store', metavar = 'NEWSAVEGAME', help = 'Output filename')
  parser.add_argument('-c', '--cash', type = int, action = 'store', metavar = 'CASHVALUE', help = 'New cash value')
  args = parser.parse_args()
  inFilename = args.savegame
  if args.output is not None:
    outFilename = args.output
  else:
    outFilename = "%s_new" % (inFilename)

  print(toolDesc + "\n")

  # Read game save file
  print("Reading game save file \"%s\" ...\n" % (inFilename))
  try:
    with open(inFilename, 'rb') as inFile:
      data = bytearray(inFile.read())
  except Exception as e:
    print("ERROR: Unable to read game save \"%s\"" % (inFilename))
    sys.exit(1)

  # Verify expected save game file size
  if len(data) != sizeSaveGame:
    print("ERROR: Unexpected save game file size ... Save is %d bytes, but tool expects %d bytes" % (len(data), sizeSaveGame))
    sys.exit(1)

  # Track existing hashes
  oldMD5A = data[0xF4F8:0xF508]
  oldCRCA = data[0x10:0x24]
  oldCRCB = data[0x24:0x38]
  oldCRCC = data[0x38:0x4C]

  # Modify save game
  if args.cash:
    oldCash = struct.unpack('<L', data[0x4069:0x406D])[0]
    data[0x4069:0x406D] = struct.pack('<L', args.cash)
    newCash = struct.unpack('<L', data[0x4069:0x406D])[0]
    print("Modified cash to %d (was %d).\n" % (newCash, oldCash))
  # TODO: Allow other items to be updated

  # Update hashes
  print("Updating hashes ...\n")
  md5A = hashlib.md5(data[0x64:0xF4F8])
  data[0xF4F8:0xF508] = md5A.digest()[0:16]
  xbeKey = hex_decode(hexXBEKey)[0]
  sigKey = hex_decode(hexSigKey)[0]
  hmacKey = hmac.new(xbeKey, sigKey, hashlib.sha1).digest()[0:16]
  crcA = hmac.new(hmacKey, data[0x4C:0x54], hashlib.sha1)
  data[0x10:0x24] = crcA.digest()[0:20]
  crcB = hmac.new(hmacKey, data[0x54:], hashlib.sha1)
  data[0x24:0x38] = crcB.digest()[0:20]
  crcC = hmac.new(hmacKey, data[0:0x38], hashlib.sha1)
  data[0x38:0x4C] = crcC.digest()[0:20]

  # Display new hashes
  newMD5A = data[0xF4F8:0xF508]
  newCRCA = data[0x10:0x24]
  newCRCB = data[0x24:0x38]
  newCRCC = data[0x38:0x4C]
  updatedMD5A = updatedCRCA = updatedCRCB = updatedCRCC = ''
  modified = False
  if newMD5A != oldMD5A:
    updatedMD5A = '[UPDATED]'
    modified = True
  if newCRCA != oldCRCA:
    updatedCRCA = '[UPDATED]'
    modified = True
  if newCRCB != oldCRCB:
    updatedCRCB = '[UPDATED]'
    modified = True
  if newCRCC != oldCRCC:
    updatedCRCC = '[UPDATED]'
    modified = True
  print('Hashes:')
  print("  %-28s  %-40s  %s" % ('Game Save Data MD5:', bytearray_hexstr(newMD5A), updatedMD5A))
  print("  %-28s  %-40s  %s" % ('Header Data HMAC-SHA1:', bytearray_hexstr(newCRCA), updatedCRCA))
  print("  %-28s  %-40s  %s" % ('Game Save Data HMAC-SHA1:', bytearray_hexstr(newCRCB), updatedCRCB))
  print("  %-28s  %-40s  %s\n" % ('Header HMAC-SHA1:', bytearray_hexstr(newCRCC), updatedCRCC))

  # Write new game save file
  print("Writing new game save file \"%s\" ...\n" % (outFilename))
  try:
    with open(outFilename, 'wb') as outfile:
      outfile.write(data)
  except Exception as e:
    print("ERROR: Unable to write game save \"%s\"" % (outFilename))
    sys.exit(1)
  if not modified:
    print("*** WARNING: SAVE GAME HASHES DID NOT CHANGE ***\n")

  print('Finished! Copy the save game to an Xbox.')
  sys.exit(0)

if __name__ == '__main__':
  main()