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

export default class GnomopoExtension extends Extension {
    onconnection(socket_service, connection, channel) {
        const istream = connection.get_input_stream(),
//            ibytes = istream.read_bytes(4, null).get_data(),
//            action = String.fromCharCode.apply(null, [ibytes]);
            datastream = new Gio.DataInputStream({ base_stream: istream }),
            action = datastream.read_line()[0];

        log("processing " + action);
        let resp, x, y, primon, geo;
        if (action == "mpos")
            [x, y] = global.get_pointer();
        else if (action == "size") { // size
            primon = global.display.get_primary_monitor();
            geo = global.display.get_monitor_geometry(primon);
            x = geo.width;
            y = geo.height;
        } else
            resp = "illegal action";
        if (!resp)
            resp = x + " " + y;
        log(action + " " + resp);
        connection.get_output_stream().write_bytes(new GLib.Bytes(resp), null);
        connection.close(null);
    }

    enable() {
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
