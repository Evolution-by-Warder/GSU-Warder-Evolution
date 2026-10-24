import contextlib
import importlib.util
import io
import pathlib
import struct
import unittest
from unittest.mock import patch

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gsu_bitrate_worker',ROOT/'src/GlassSysUtil/bitrate_worker.py')
worker=importlib.util.module_from_spec(spec);spec.loader.exec_module(worker)


class WorkerTests(unittest.TestCase):
    def test_transport_filter_and_buffer_use_separate_readonly_fd(self):
        with patch.object(worker.os,'open',return_value=17) as op,patch.object(worker.fcntl,'ioctl') as ioctl:
            self.assertEqual(worker.open_reader(0,0,3001),17)
            self.assertEqual(op.call_args.args,('/dev/dvb/adapter0/demux0',worker.os.O_RDONLY|worker.os.O_NONBLOCK))
            self.assertEqual(ioctl.call_args_list[0].args,(17,worker.DMX_SET_BUFFER_SIZE,1048576))
            self.assertEqual(struct.unpack('=H2xIIII',ioctl.call_args_list[1].args[2]),(3001,0,3,20,4))

    def test_failed_filter_closes_fd_and_missing_pid_opens_nothing(self):
        with patch.object(worker.os,'open',return_value=17) as op,patch.object(worker.os,'close') as close,patch.object(worker.fcntl,'ioctl',side_effect=OSError(22,'unsupported')):
            with self.assertRaises(OSError):worker.open_reader(0,0,3001)
            close.assert_called_once_with(17)
            self.assertIsNone(worker.open_reader(0,0,-1))
            self.assertEqual(op.call_count,1)

    def test_fragmented_reads_and_overflow_do_not_lose_other_ready_bytes(self):
        errors=[OSError(worker.errno.EOVERFLOW,'overflow'),b'123',b'4567',BlockingIOError()]
        with patch.object(worker.os,'read',side_effect=errors):self.assertEqual(worker.read_ready(17),7)

    def test_two_pid_sampling_outputs_rates_and_closes_on_stop(self):
        output=io.StringIO()
        with patch.object(worker,'open_reader',side_effect=[17,18]),patch.object(worker,'read_ready',side_effect=[100000,25000,200000,25000]),patch.object(worker.select,'select',side_effect=[([17,18],[],[]),([17,18],[],[]),KeyboardInterrupt()]),patch.object(worker.time,'monotonic',side_effect=[0,0,1,1,2,2]),patch.object(worker.os,'close') as close,contextlib.redirect_stdout(output):
            with self.assertRaises(KeyboardInterrupt):worker.main(['0','0','3001','3011'])
        self.assertEqual(output.getvalue().splitlines(),['800 800 800 800','200 200 200 200','800 1600 1200 1600','200 200 200 200'])
        self.assertEqual({c.args[0] for c in close.call_args_list},{17,18})
