import os
import Queue
from logging import Handler, StreamHandler
from logging.handlers import TimedRotatingFileHandler
import time
from portalocker import lock, unlock, LOCK_EX, LOCK_NB, LockException
from static import log_path

FORCE_ABSOLUTE_PATH = False

# ---------------------------------------------------------------------------
#   Miscellaneous module data
# ---------------------------------------------------------------------------
try:
    unicode
    _unicode = True
except NameError:
    _unicode = False


class OpendsStreamHandler(StreamHandler):
    def _emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.format(record)
            stream = self.stream
            fs = "%s\n"
            if not _unicode:  # if no unicode support...
                stream.write(fs % msg)
            else:
                try:
                    if isinstance(msg, unicode) and getattr(stream, 'encoding', None):
                        ufs = u'%s\n'
                        try:
                            stream.write(ufs % msg)
                        except UnicodeEncodeError:
                            # Printing to terminals sometimes fails. For example,
                            # with an encoding of 'cp1251', the above write will
                            # work if written to a stream opened or wrapped by
                            # the codecs module, but fail when writing to a
                            # terminal even when the codepage is set to cp1251.
                            # An extra encoding step seems to be needed.
                            stream.write((ufs % msg).encode(stream.encoding))
                    else:
                        stream.write(fs % msg)
                except UnicodeError:
                    stream.write(fs % msg.encode("UTF-8"))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


