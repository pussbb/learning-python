# -*- coding: utf-8 -*-
"""
"""
import pywbxml


xml_str = b"""<?xml version="1.0"?>
<!DOCTYPE ActiveSync PUBLIC "-//MICROSOFT//DTD ActiveSync//EN" "http://www.microsoft.com/">
<Sync>
  <Collections>
    <Collection>
      <Class>Contacts</Class>
      <SyncKey>9</SyncKey>
      <CollectionId>00010a029c1a3275</CollectionId>
      <DeletesAsMoves />
      <GetChanges />
      <WindowSize>4</WindowSize>
      <Options>
        <BodyPreference>
          <Type>1</Type>
          <TruncationSize>200000</TruncationSize>
        </BodyPreference>
      </Options>
      <Commands>
        <Add>
          <ClientId>new_7_1470740796131</ClientId>
          <ApplicationData>
            <MobilePhoneNumber>34324324324</MobilePhoneNumber>
            <LastName>Fsdfdsf</LastName>
            <FirstName>Sfds</FirstName>
          </ApplicationData>
        </Add>
        <Add>
          <ClientId>new_7_1470740796138</ClientId>
          <ApplicationData>
            <MobilePhoneNumber>(734) 234-234</MobilePhoneNumber>
            <LastName>Werewrwerewrwe</LastName>
            <FirstName>Ewrewr</FirstName>
            <Email1Address>"34234324" &lt;34234324&gt;</Email1Address>
          </ApplicationData>
        </Add>
      </Commands>
    </Collection>
  </Collections>
</Sync>
"""

print(pywbxml.xml2wbxml(xml_str))
print(pywbxml.wbxml2xml(pywbxml.xml2wbxml(xml_str)))
