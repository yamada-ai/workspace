import { UserState } from './UserState';

export class UserModel {
  constructor(
    public readonly id: string,
    public name: string,
    public icon: string,
    public state: UserState = UserState.Idle,
  ) {}

  canDance(): boolean {
    return this.state === UserState.Idle;
  }

  dance(): UserModel {
    if (!this.canDance()) return this;
    return new UserModel(this.id, this.name, this.icon, UserState.Dancing);
  }

  reset(): UserModel {
    return new UserModel(this.id, this.name, this.icon, UserState.Idle);
  }
}
