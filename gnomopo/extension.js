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
	console.debug("gnomopo: " + msg);
};

export default class PlainExampleExtension extends Extension {
    onconnection(socket_service, connection, channel) {
        const [x, y] = global.get_pointer(),
            pos = x + " " + y;
        log("mouse at " + pos);
        connection.get_output_stream().write_bytes(new GLib.Bytes(pos), null);
        connection.close(null);
    }

    getservice() {
        if (!this._service) {
            this._service = new Gio.SocketService();
            this._service.add_address(socket_address, Gio.SocketType.STREAM, Gio.SocketProtocol.DEFAULT, null);
            this._service.connect('incoming', this.onconnection);
            log("initialized service on port " + port);
        }
        return this._service;
    }

    enable() {
        log("starting")
        this.getservice().start();
    }

    disable() {
        log("stopping")
        this.getservice().close();
    }
}
