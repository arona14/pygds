# """
#     This is for testing purposes like a suite.
# """
# import logging
# from pygds.core.security_utils import decode_base64
# from pygds.env_settings import get_setting
# from pygds.sabre.client import SabreClient
# import os


# def test():
#     """ A suite of tests """

#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     dir_path = os.path.join(dir_path, "..", "..", "..")
#     os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)

#     username = get_setting("SABRE_USERNAME")
#     pcc = get_setting("SABRE_PCC")
#     password = decode_base64(get_setting("SABRE_PASSWORD"))
#     url = "https://webservices3.sabre.com"
# <<<<<<< HEAD
#     pnr = "GOQOBU"  # "TGZKPI"
#     client = SabreClient(url, "", username, password, pcc, False)
#     retrieve_pnr = client.get_reservation(pnr, None, True)
#     logging.error(retrieve_pnr.payload)
# =======
#     # pnr = "TGZKPI"
#     client = SabreClient(url, "", username, password, pcc, False)
# <<<<<<< Updated upstream
#     message_id = None
#     client.get_or_create_session_details(message_id)
# =======
#     retrieve_pnr = client.get_reservation("GOQOBU", None, True)
#     print(retrieve_pnr.payload)
# >>>>>>> Stashed changes
# >>>>>>> 3b3a96fbfccc1cd9be19356c1b9b26e18eb596d4


# if __name__ == "__main__":
#     test()
