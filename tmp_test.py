def gen():
    print('here1')
    print('here2')
    while True:
        sent_in = yield
        try:
            if sent_in == 'def':
                raise OSError
        except:
            print('exception handled')
        print('in gen:', sent_in)

gen_1 = gen()
gen_1.send(None)
gen_1.send('abc')
gen_1.send('def')
gen_1.send('ghi')