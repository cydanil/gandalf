import pkg_resources

import zulip


class Gandalf:
    def __init__(self):
        self.client = zulip.Client(config_file="zuliprc")
        self.name = self.client.get_profile()['full_name']
        self.client.add_subscriptions([{"name": "test_stream2"}])

        self.commands = {
            ep.name: ep.load()
            for ep in pkg_resources.iter_entry_points("gandalf_reply_scripts")
        }

        self.client.call_on_each_message(self.handler)

    def handler(self, msg: dict) -> int:
        content = msg["content"]
        sender = msg["sender_email"]
        subject = msg["subject"]
        stream = msg["display_recipient"]
        msg_type = msg["type"]

        if sender == self.client.email:
            return

        target = content.split()[0]

        if not (
            self.name in target
            or any(r["full_name"] == self.name for r in msg["display_recipient"])
        ):
            return

        if self.name in target:  # Strip name
            _, content = content.split(maxsplit=1)

        to = stream if isinstance(stream, str) else sender

        command, *arguments = content.split(maxsplit=1)

        try:
            reply = self.commands[command](arguments)
        except KeyError:
            reply = f"Available commands are {self.commands.keys()}"
        except Exception as e:
            reply = f"`{command}` failed with `{arguments}`:\n `{e}`"

        self.client.send_message(
            {
                "type": msg_type,
                "to": to,
                "subject": subject,
                "content": reply,
            }
        )


def main():
    gandalf = Gandalf()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
