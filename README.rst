.. image:: https://travis-ci.org/RobbieClarken/channelarchiver.svg
    :target: https://travis-ci.org/RobbieClarken/channelarchiver

A python client for retrieving data from an EPICS Channel Archiver.

To get started just import the ``Archiver`` class and specify the
address of your Channel Archiver server:

.. code:: python

    from channelarchiver import Archiver
    archiver = Archiver('http://xf23id-ca/cgi-bin/ArchiveDataServer.cgi')

You then fetch data with the ``archiver.get()`` method:

.. code:: python

    >>> data = archiver.get('XF:23IDA-VA:0{DP:1-IP:1}P-I', '2013-08-11', '2014-08-12')
    >>> print(data)
                   time  value    status     severity
                   2014-06-28 22:11:53      0  NO_ALARM  ARCHIVE_OFF

    ...
    >>> data.values
    [0.0]

The returned ``ChannelData`` object has the following fields:

-  ``channel``: The channel name.
-  ``times``: A list of datetimes.
-  ``values``: A list of the channel's values corresponding to
   ``times``.
-  ``severities`` and ``statuses``: Diagnostic information about the
   channel state for each time.
-  ``units``: The units of ``values``.
-  ``states``: String values for enum type channels.
-  ``data_type``: Whether the channel values are string, enum, int or
   double (see ``codes.data_type``).
-  ``elements``: The number of elements in an array type channel.
-  ``display_limits``, ``warn_limits``, ``alarm_limits``: Low and high
   limits
-  ``display_precision``: The recommended number of decimal places to to
   display values with in user interfaces.
-  ``archive_key``: The archive the data was retrieved from.
-  ``interpolation``: The interpolation method that was used (see
   ``codes.interpolation``).

Get multiple channels
~~~~~~~~~~~~~~~~~~~~~

If you pass a list of channel names to ``.get()`` you will get a list of
data objects back:

.. code:: python

    >>> channels = ['XF:23IDA-VA:0{DP:1-IP:1}P-I', ' XF:23IDA-VA:0{DP:1-CCG:1}P-I']
    >>> x, y = archiver.get(channels, '2013-08-24 09:00', '2014-08-24 19:00')
    >>> print(x.values)
    [ 0.0]
    >>> print(y.values)
    []

Times and timezones
~~~~~~~~~~~~~~~~~~~

The start and end times over which to fetch data can be datetimes
or strings in ISO 8601 format (eg ``2013-08-10T21:30:00``).

If no timezone is specified, your local timezone will be used. If a timezone is given,
the returned channel data times will also be in this timezone.

.. code:: python

    >>> start = datetime.datetime(2012, 6, 1, tzinfo=pytz.UTC)
    >>> end = datetime.datetime(2012, 6, 30, tzinfo=pytz.UTC)
    >>> data_in_utc = archiver.get('BR00EXS01:TUNNEL_TEMPERATURE_MONITOR', start, end)

Interpolating
~~~~~~~~~~~~~

You can control how much data is returned from the archiver with the
``limit`` parameter. This is roughly equal to how many data points will
be returned but the actual value will differ depending on how much data is
available and the interpolation method.

The interpolation method is determined by the ``interpolation`` parameter. The
allowed values are the ``'raw'``, ``'spreadsheet'``, ``'averaged'``, ``'plot-binning'``
and ``'linear'``. The default value is ``'linear'``.

.. code:: python

    >>> from channelarchiver import codes
    >>> channel = 'SR00MOS01:FREQUENCY_MONITOR'
    >>> data = archiver.get(channel, '2012', '2013', limit=10000, interpolation='raw')

Speeding up data retrieval
~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, for each ``.get`` call ``Archive`` will scan the archives to
determine which one contains data for the specified channels. This will
cause a slight delay in retrieving the data. This can be avoided by
calling the ``.scan_archives()`` method once and then passing
``scan_archives=False`` to ``.get()``:

.. code:: python

    >>> archiver.scan_archives()
    >>> d1 = archiver.get('XF:23IDA-VA:0{DP:1-IP:1}P-I', '2013-07', '2014-08', scan_archives=False)
