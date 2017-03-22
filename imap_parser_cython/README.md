 
```shell
time python3 ./fetch_.py 
Lock acquired  MainThread 2017-03-22T14:48:31.791870
1:* (BODYSTRUCTURE FLAGS INTERNALDATE ENVELOPE UID RFC822.SIZE)
/opt/hg/scalix_server/scalix13/sxmail/sxmail/imap/_lockable.py:118: RuntimeWarning: Data left {'READ-WRITE': [b''], 'EXISTS': [b'1984'], 'OK': [b'[UNSEEN 1984] is the first unread message', b'[UIDVALIDITY 1] UIDVALIDITY value', b'[UIDNEXT 284649] Predicted next UID', b'[PERMANENTFLAGS (\\Answered \\Flagged \\Deleted \\Seen \\Draft $Label1 $Label2 $Label3 $Label4 $Label5 $Forwarded Junk NonJunk X-Scalix-Processed $MdnSent)] flags will stay set']}
  warnings.warn('Data left {}'.format(self.last_untagged_responses), RuntimeWarning)
1984
Lock released  MainThread 2017-03-22T14:48:36.103327
Lock acquired  Dummy-1 2017-03-22T14:48:36.114112
Lock released  Dummy-1 2017-03-22T14:48:36.114286

real    0m5,986s
user    0m1,960s
sys     0m0,112s

```
