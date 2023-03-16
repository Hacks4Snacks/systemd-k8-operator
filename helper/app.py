from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/systemd-unit-status', methods=['GET'])
def systemd_unit_status():
    unit_name = request.args.get('unitName')
    if not unit_name:
        return jsonify({'error': 'unitName parameter is required'}), 400

    try:
        output = subprocess.check_output(['systemctl', 'show', unit_name, '--no-page'])
        properties = output.decode('utf-8').split('\n')
        status_info = {}
        for prop in properties:
            if prop.startswith('ActiveState=') or prop.startswith('UnitFileState='):
                key, value = prop.split('=')
                status_info[key] = value

        unit_status = f"{status_info['ActiveState']};{status_info['UnitFileState']}"
        return jsonify({'unitName': unit_name, 'unitStatus': unit_status})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

