import { Area } from '../area/Area';
import { ID } from '../ID';
import { UserState } from './UserState';

export class UserModel {
  constructor(
    public readonly id: ID<UserModel>,
    public name: string,
    public work_name: string | null,
    public icon: string,
    public state: UserState = UserState.Idle,
    public area: Area = Area.Tier3
  ) {}

  copyWith(update: Partial<Omit<UserModel, 'id'>>): UserModel {
    return new UserModel(
      this.id,
      update.name ?? this.name,
      update.work_name ?? this.work_name,
      update.icon ?? this.icon,
      update.state ?? this.state,
      update.area ?? this.area
    );
  }

  canDance(): boolean {
    return this.state === UserState.Idle ;
  }

  dance(): UserModel {
    if (!this.canDance()) return this;
    return this.copyWith({ state: UserState.Dancing });
  }

  canWalk(): boolean {
    return this.state === UserState.Idle || this.state === UserState.Walking
  }

  walk(): UserModel {
    if (!this.canWalk()) return this;
    return this.copyWith({ state: UserState.Walking });
  }

  reset(): UserModel {
    return this.copyWith({ state: UserState.Idle });
  }
}
