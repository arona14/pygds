# """
#     This is for testing purposes like a suite.
# """
# from pygds import log_handler
# from pygds.env_settings import get_setting
# import os
# import fnc
# from pygds.amadeus.client import AmadeusClient
# from pygds.amadeus.errors import ClientError, ServerError
# # from pygds.core.types import TravellerInfo, ReservationInfo


# def test():
#     """ A suite of tests """
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
#     client = AmadeusClient(endpoint, username, password, office_id, wsap, True)
#     pnr = 'O95J97'  # "LTGPDG"
#     try:

#         message_id = None
#         log.info("1. Retrieve PNR")
#         res_reservation = client.get_reservation(pnr, message_id, False)
#         res_reservation, session_info = res_reservation.payload, res_reservation.session_info
#         # log.info(res_reservation)
#         # log.info(session_info)
#         if session_info.session_ended is True:
#             log.debug("Session is ended after retrieve PNR")
#             return
#         message_id = session_info.message_id

#         email_tato = ""
#         for ot in res_reservation["other_information"]:
#             if fnc.get("otherDataFreetext.freetextDetail.type", ot) == "P02":
#                 email_tato = ot["elementManagementData"]["reference"]["number"]
#         log.info("2. Update passenger")
#         if email_tato != "":
#             response = client.cancel_information_passenger(email_tato, message_id)
#             log.info(response)
#         passengers = [p.name_id for p in res_reservation["passengers"]]
#         # for pr in passengers:
#         # log.info(f"begin  of Calling update Passenger Information for passenger {pr} **")
#         # res_updat_pas = client.pnr_add_multi_for_pax_info_element(message_id, "Amadou1994@gmail.com", passengers[0], office_id)
#         res_updat_pas, session_info = res_updat_pas.payload, res_updat_pas.session_info
#         log.debug(res_updat_pas)
#         # log.debug(session_info)
#         if session_info.session_ended is True:
#             log.debug("Session closed after update passenger")
#             return
#         message_id = session_info.message_id

#         if session_info.session_ended is False:
#             log.info("3. Close session")
#         client.close_session(message_id)
#     except ClientError as ce:
#         log.error(f"client_error: {ce}")
#         log.error(f"session: {ce.session_info}")
#     except ServerError as se:
#         log.error(f"server_error: {se}")
#         log.error(f"session: {se.session_info}")


# # if __name__ == "__main__":
# #     test()