# """
#     This is for testing purposes like a suite.
# """

# from pygds import log_handler
# from pygds.env_settings import get_setting
# import os
# from pygds.amadeus.client import AmadeusClient
# from pygds.amadeus.errors import ClientError, ServerError


# def test():
#     # This is not a test file. It is just used to locally test a flow
#     endpoint = get_setting("AMADEUS_ENDPOINT_URL")
#     username = get_setting("AMADEUS_USERNAME")
#     password = get_setting("AMADEUS_PASSWORD")
#     office_id = get_setting("AMADEUS_OFFICE_ID")
#     wsap = get_setting("AMADEUS_WSAP")
#     dir_path = os.path.dirname(os.path.realpath(__file__))
#     dir_path = os.path.join(dir_path, "..", "..", "..")
#     os.makedirs(os.path.join(dir_path, "out"), exist_ok=True)
#     log_handler.load_file_config(os.path.join(dir_path, "log_config.yml"))
#     log = log_handler.get_logger("test_all")
#     pnr = "LCD4TN"

#     client = AmadeusClient(endpoint, username, password, office_id, wsap, True)
#     try:
#         message_id = None
#         res_reservation = client.get_reservation(pnr, message_id, False)
#         session_info, res_reservation = (res_reservation.session_info, res_reservation.payload)
#         log.info(session_info)
#         log.info(res_reservation)
#         # client.get_or_create_session_details(message_id)
#     except ClientError as ce:
#         log.error(f"client_error: {ce}")
#         log.error(f"session: {ce.session_info}")
#     except ServerError as se:
#         log.error(f"server_error: {se}")
#         log.error(f"session: {se.session_info}")


# # if __name__ == "__main__":
# #     test()
