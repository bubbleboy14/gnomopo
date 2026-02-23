/* extension.js
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

const port = 62090,
    socket_address = Gio.InetSocketAddress.new_from_string('127.0.0.1', port);

const log = function(msg) {
	console.log("gnomopo: " + msg);
};

const rectify = function(rect) {
    return {
        x: rect.x, y: rect.y, width: rect.width, height: rect.height
    };
};

class Gnomopo {
    mpos() {
        return global.get_pointer().join(" ");
    }

    size() {
        const primon = global.display.get_primary_monitor(),
            geo = global.display.get_monitor_geometry(primon),
            coords = [geo.width, geo.height, primon.geometry_scale || 1];
        return coords.join(" ");
    }

    window() {
        const fwin = global.display.get_focus_window();
        return JSON.stringify({
            "frame": rectify(fwin.get_frame_rect()),
            "buffer": rectify(fwin.get_buffer_rect())
        });
    }

    process(action) {
        if (! ["mpos", "size", "window"].includes(action))
            return "illegal action";
        return this[action]();
    }
}

class GnoConn {
    close(err) {
        this.connection.close(null);
        if (err)
            log("closed with error: " + err);
        else
            log("closed");
        delete this.connection;
        delete this.datastream;
        delete this.proc;
    }

    check(now) {
        if (now - this.ts > 60000) {
            log("timed out");
            return this.close.call(this, "timeout");
        }
        return true;
    }

    read(stream, res) {
        this.ts = Date.now();
        try {
            const [line, length] = stream.read_line_finish(res);
            if (length == 0 || line === null)
                return this.close.call(this);
            const action = line.toString().trim(), resp = this.proc(action);
            log(action + " " + resp);
            this.connection.get_output_stream().write_bytes(new GLib.Bytes(resp), null);
        } catch (e) {
            return this.close.call(this, e.message);
        }
        this.listen.call(this);
    }

    listen() {
        this.datastream.read_line_async(GLib.PRIORITY_DEFAULT, null, this.read.bind(this));
    }

    manage(connection, proc) {
        log("opened");
        this.proc = proc;
        this.ts = Date.now();
        this.connection = connection;
        this.datastream = new Gio.DataInputStream({
            base_stream: connection.get_input_stream()
        });
        this.listen.call(this);
    }
}

export default class GnomopoExtension extends Extension {
    onconnection(socket_service, connection, channel) {
        this._connid += 1;
        const conn = this._conns[this._connid] = new GnoConn();
        conn.manage.call(conn, connection, this._gnomopo.process.bind(this._gnomopo));
        return true;
    }

    check() {
        const now = Date.now(), closed = [];
        let connid, conn;
        for (connid in this._conns) {
            conn = this._conns[connid];
            if (!conn.check.call(conn, now))
                closed.push(connid);
        }
        for (connid of closed)
            delete this._conns[connid];
        return true;
    }

    closeall() {
        const connids = Object.keys(this._conns);
        let connid, conn;
        for (connid of connids) {
            conn = this._conns[connid];
            delete this._conns[connid];
            conn.close.call(conn);
        }
    }

    enable() {
        this._conns = {};
        this._connid = 0;
        this._gnomopo = new Gnomopo();
        this._service = new Gio.SocketService();
        this._service.add_address(socket_address, Gio.SocketType.STREAM, Gio.SocketProtocol.DEFAULT, null);
        this._service.connect('incoming', this.onconnection.bind(this));
        this._service.start();
        this._timeout = GLib.timeout_add(GLib.PRIORITY_DEFAULT, 10000, this.check.bind(this));
        log("enabled on port " + port)
    }

    disable() {
        this.closeall.call(this);
        if (this._timeout)
            GLib.Source.remove(this._timeout);
        if (this._service) {
            this._service.stop();
            this._service.close();
            this._service = null;
        }
        this._gnomopo = null;
        log("disabled")
    }
}
