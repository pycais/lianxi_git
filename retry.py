from retrying import retry, Retrying

count = 0


@retry(stop_max_attempt_number=6, wait_fixed=1000)
def aaa():
    global count
    count += 1
    print(count)
    raise 'dw'

aaa()
