import { SessionStartEvent, SessionEndEvent } from "../../domain/ws/WsEvent";
import { UserModel } from "../../domain/user/UserModel";
import { ID } from "../../domain/ID";
import { UserState } from "../../domain/user/UserState";
import { Area } from "../../domain/area/Area";
import { registerUser } from "../../app/registerUser";
import { useUserViewStore } from "../cache/UserViewStore";

// セッション開始時の処理
export function handleSessionStart(msg: SessionStartEvent) {
  const { setComment } = useUserViewStore.getState();

  const user = new UserModel(
    msg.id as ID<UserModel>,
    msg.user_name,
    msg.work_name, 
    "princess.png",
    UserState.Idle,
    Area.Tier1
  );
  registerUser(user);
  setComment(user.id, `${msg.user_name}が「${msg.work_name}」開始`);
}

// （例）セッション終了時の処理
export function handleSessionEnd(msg: SessionEndEvent) {
//   const { removeUser } = useUserStore.getState();
//   removeUser(msg.id as ID<UserModel>);
    console.log(msg)
    return
}
