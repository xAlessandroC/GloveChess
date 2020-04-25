import glut_application as glta
from model_utils import *
from executer import *

from_f = None
to_f = None
last_selected_f = None
logic_state = "FROM"

def extract_move(fingers):
    # Ipotizziamo che in fingers non ci siano dati spuri
    global logic_state, from_f, to_f, last_selected_f

    result = False

    # print("[HUMAN_PLAYER]: extracted ", fingers)
    fingers_number = len(fingers)

    if fingers_number >= 5:
        # Movimento puntatore
        selected_finger = fingers[2]
        # last_selected = FUNZIONE(selected_finger)
        glta.queue_A.put(selected_finger)
        # print("[HUMAN PLAYER]: Mandato su A",selected_finger,"]")
        t = glta.queue_B.get()
        if t != None:
            last_selected_f = t
        # print("[HUMAN PLAYER]: Ricevuto da B",last_selected_f,"]")

    elif fingers_number == 2:
        # Selezione cella
        if logic_state == "FROM" and last_selected_f != None:
            print("[HUMAN PLAYER]: selected from ", last_selected_f)
            from_f = last_selected_f
            logic_state = "TO"

        elif logic_state == "TO" and last_selected_f != from_f:
            print("[HUMAN PLAYER]: selected to ", last_selected_f)
            to_f = last_selected_f
            logic_state = "FROM"

        if from_f != None and to_f != None and last_selected_f != None:
            ##EXECUTE(from_f, to_f)
            from_m = from_matrix_to_chessboard(from_f)
            to_m = from_matrix_to_chessboard(to_f)
            print("[HUMAN PLAYER]: faccio mossa ", from_f, to_f)
            try:
                checkAndExecuteMove(from_m, to_m)
                result = True
            except:
                pass

            from_f = None
            to_f = None


    return result
