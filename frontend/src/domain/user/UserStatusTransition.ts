import { UserState } from "./UserState";

export class UserStatusTransition {
    static canTransition(from: UserState, to: UserState): boolean {
      if (from === UserState.Dancing && to !== UserState.Idle) return false;
      return true;
    }
  
    static nextFromCommand(command: string): UserState {
      switch (command) {
        case '/dance': return UserState.Dancing;
        case '/sleep': return UserState.Sleeping;
        default: return UserState.Idle;
      }
    }
  }
  