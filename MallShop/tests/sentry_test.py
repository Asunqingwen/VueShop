dsn = "http://e2a9ff04318743b9b55e7b2be7d80d3c@47.103.86.8:9000/3"

import sentry_sdk

sentry_sdk.init(dsn)

division_by_zero = 1 / 0
