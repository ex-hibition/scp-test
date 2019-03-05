import logging
import os
from paramiko import SSHClient, AutoAddPolicy


class Cooperation:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        _formatting = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=_formatting)
        logging.getLogger("paramiko").setLevel(level=logging.INFO)

        # docker:centos7:cent7
        self.info = {
            'ip_address': '0.0.0.0',
            'port': 2222,
            'username': 'scpuser',
            'password': 'scpuser',
        }

    def ssh_exec(self, target: str):
        """sshファイル取得"""
        # sshオブジェクト生成
        with SSHClient() as ssh:
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(hostname=self.info["ip_address"],
                        port=self.info["port"],
                        username=self.info["username"],
                        password=self.info["password"])

            # ファイルリスト取得
            sftp = ssh.open_sftp()
            file_list = sftp.listdir('.')
            self.logger.debug(f"list={file_list}")

            # .ENDファイル存在チェック
            if [x for x in file_list if f"{target}.END" in x]:
                self.logger.debug(f"checked={target}.END")
                # sftp.get(target, os.path.join('downloads', target))
            else:
                raise Exception(f"指定ファイルが存在しない: {target}.END")

            # データファイル存在チェック
            if [x for x in file_list if target in x]:
                sftp.get(target, os.path.join('downloads', target))
                self.logger.debug(f"get={target}")
            else:
                raise Exception(f"指定ファイルが存在しない: {target}")

            # ENDファイル削除
            sftp.remove(f"{target}.END")
            self.logger.debug(f"removed={target}.END")


if '__main__' == __name__:
    obj = Cooperation()
    obj.ssh_exec(target='test1.txt')




