import hashlib

sign = "xiaon"


def sign_md5(*args):
    field_args = '&'.join(args)
    print(field_args)
    s = hashlib.md5(field_args.encode("utf-8")).hexdigest()

    md5str_sign = '{}&{}'.format(s, sign)
    md5str = hashlib.md5(md5str_sign.encode("utf-8")).hexdigest()
    print(md5str)
    return md5str
