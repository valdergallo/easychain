# easychain: 
*based (https://github.com/davecan/easychain)*

This is the result of a bit of research and some tinkering to understand the fundamental concepts of a blockchain. Readers are directed to Ilya Gritorik's fantastic [Minimum Viable Blockchain](https://www.igvita.com/2014/05/05/minimum-viable-block-chain/) article for more general information about what blockchains are and how they work conceptually.

# Example

This is a quick example. A more detailed example (including hostile tampering and detection) is in `example.py`. There are also a few basic unit tests.

    msg1 = Message("simple message")
    msg2 = Message("with a sender and receiver", "Alice", "Bob")

    # each of the above now has a hashed payload, link them by adding to a block

    block1 = Block()
    block1.add_message(msg1)
    block1.add_message(msg2)

    # or using the constructor

    block1 = Block(msg1, msg2)

    # messages are now fully hashed and linked, msg2 depends on msg1, tampering can be detected

    block2 = Block()
    block2.add_message(Message("just need a second block for an example"))

    # now link the blocks together

    chain = Blockchain()
    chain.add_block(block1)
    chain.add_block(block2)

    # now the blocks are linked, block2 depends on block1

    # the hash will auto calculated if anything change in messages

    In [1]: from easychain.blockchain import *
    In [2]: %cpaste
    Pasting code; enter '--' alone on the line to stop or use Ctrl-D.
    :def get_messages(*args):
    :    content = []
    :    last_msg = None
    :    for arg in args:
    :        msg = Message(arg)
    :        content.append(msg)
    :        if last_msg:
    :            msg.link(last_msg)
    :        last_msg = msg
    :    return content
    :<EOF>
    In [3]: msgs = get_messages("first", "second", "third", "fourth", "fifth")

    In [4]: [i.hash for i in msgs]
    Out[4]:
    ['576c7599ac25730b29fe334537f4e63c6cd6df168c5f130ebb574ff01fa44c80',
     '2ceff64c8304e51efb14a23ed3f56fc2331ed98b04db3c0901dc1c487fe6a402',
     '60f4c82e01a1523edc0f0dda4e55c385483f61fcc51f9c23f31caeedfe6533f4',
     '65f520f38d67b17edca6e2e02b7e5c2bc12048a018d23ebc88bd6fd3ab7fc23c',
     '05c98be26168e6b23d24b990a2cabbe053e05106ff147f52a713f3f89f47fde3']

    In [5]: msgs[1].data = 'changed'

    In [6]: [i.hash for i in msgs]
    Out[6]:
    ['576c7599ac25730b29fe334537f4e63c6cd6df168c5f130ebb574ff01fa44c80',
     '4571d216f229ff85816ba0a09b7a26e01c66ab6d0468e5ef224e8a001e36bb2e',
     'fa4c9bea8f0025295f248c6ad3bd4caf31c9a8aebae0cf19a8c508642a2e5500',
     '531a69e94f4b43d4a874d90b7e6aadcb22004d1d10080e10a935c3d628c67fb4',
     '84d94084e4278fb178a46b659f4db99720df9b32ace217b6fd05c69dd062abf8']



# What it isn't

This implementation focuses *only* on the hashed ledger concept. It specifically does not include any concept of mining or any other form of
distributed consensus. It also abstracts the concept of a transaction to that of a message in general, narrowing the scope to a blockchain as a cryptographic primitive instead of as a method of distributed consensus. The concept of a header and payload in messages and blocks is adapted from Bitcoin.

Note that the entire point of a blockchain is to provide a mechanism for distributed consensus. This is typically accomplished through a proof-of-work mechanism. Bitcoin requires the network to engage in significant computational effort by way of a cryptographic puzzle competition in order to create a block (this is the *mining* part of Bitcoin). The computer that solves the puzzle creates the next block, marking it with the answer to the puzzle and distributing the block to all other computers. The winning computer is also awarded a prize of bitcoins. (currently 12.5 bitcoins) It is a strict constraint of the Bitcoin system that all participating nodes only accept the block that contains the answer to the puzzle, and also that all nodes accept the longest chain of valid blocks as the "correct" blockchain. Anything else allows attackers to exploit the system and commit fraud, destroying the entire system. See [Satoshi Nakamoto's e-mail response](http://satoshi.nakamotoinstitute.org/emails/cryptography/6/) for more details on why.

So understand that while this project is helpful in explaining how the blockchain is **structured** it does not in any way address how it **operates** in a network such as Bitcoin. In that sense this is analyzing the **static semantics of the blockchain**, not its *dynamic* semantics. ([more on semantics](http://cs.lmu.edu/~ray/notes/plspec/)) Doing that would require writing client code that would send out transactions and listen for them on the network, include a means for synchronizing a puzzle to be solved, work to solve the puzzle, package the outstanding transactions into a block once the puzzle is solved, distribute the block to the rest of the network, and robustly deal with bad transactions and blocks when they arrive.

# Classes

Conceptually it works somewhat like this image from [Satoshi Nakamoto's original Bitcoin paper](https://bitcoin.org/bitcoin.pdf). (incidentally if you haven't read it, its utterly brilliant, only nine pages, and much more approachable than you think)

![simplified bitcoin blockchain](https://i.imgur.com/hZObTJN.png)
