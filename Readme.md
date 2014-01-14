LogPapa
================

**LogPapa** is a python library, for reducing log analysising and statisticing work.

## Quick Start

To statistic a plain(date tail) log, you can create a `DateTailLogProcessor` object and initialize and use it like this:

```python
from LogPapa.processor import DateTailLogProcessor

log_proc = DateTailLogProcessor(
    "ERROR", 
    result_file = "./WebError-Result/%s.csv" % utils.get_last_day_date_str(), 
    ignore_info_regix = [r"[\w\W]+ \[[\w\W]+\]"],
    file_glob = "./WebErrorLog/WebError*")

log_proc.process()
```

The log info is like this(here is only one log line for example):
```
【2014-01-13 20:52:59,818】 [58] ERROR WebErrorLogger - 对于“Ihou.UserDomain.Controllers.UserDomainController”中方法“System.Web.Mvc.ActionResult ContentCenterOneCover(Int64, System.Nullable`1[System.Int32], System.String, System.Nullable`1[System.Int32], System.String)”的不可以为 null 的类型“System.Int64”的参数“userHashId”，参数字典包含一个 null 项。可选参数必须为引用类型、可以为 null 的类型或声明为可选参数。
```

The log processor will do these things:
 - read log files(`by the glob string parameter: @file_glob`) 
 - extract all the useful line(`by the first parameter: @key_regex`)
 - statistic the times of every log type(`by the parameter: @stat_regex, default="[\w\W]*"`)
 - write a statistic result file like this(`csv file`):
```
ERROR WebErrorLogger - 未将对象引用设置到对象的实例。【60.166.58.226】
【http://www.ihou.com/Sing/SongProgramList】,2
```

## Contract me
**LogPapa** is in developing, if you have any suggestion, please contract me: 

Email: weatherpop@gmail.com

QQ: 623891205

Thanks a lot~
:)