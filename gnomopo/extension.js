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

export default class GnomopoExtension extends Extension {
    onconnection(socket_service, connection, channel) {
        const datastream = new Gio.DataInputStream({
            base_stream: connection.get_input_stream()
        }), proc = this._gnomopo.process.bind(this._gnomopo);
        log("opened");
        datastream.read_line_async(GLib.PRIORITY_DEFAULT, null, (stream, res) => {
            try {
                const [line, length] = stream.read_line_finish(res);
                if (length == 0 || line === null) {
                    connection.close(null);
                    return log("closed");
                }
                const action = line.toString().trim(), resp = proc(action);
                log(action + " " + resp);
                connection.get_output_stream().write_bytes(new GLib.Bytes(resp), null);
            } catch (e) {
                connection.close(null);
                log("closed with error: " + e.message);
            }
        });
        return true;
    }

    enable() {
        this._gnomopo = new Gnomopo();
        this._service = new Gio.SocketService();
        this._service.add_address(socket_address, Gio.SocketType.STREAM, Gio.SocketProtocol.DEFAULT, null);
        this._service.connect('incoming', this.onconnection.bind(this));
        this._service.start();
        log("enabled on port " + port)
    }

    disable() {
        if (this._service) {
            this._service.stop();
            this._service.close();
            this._service = null;
        }
        log("disabled")
    }
}
