import { Router, RouterModule } from '@angular/router';

//import { MapComponent } from '../map/map.component';
import { AdminUserComponent } from '../admin/user/admin-user.component';

export const navbarRouting = RouterModule.forChild([
    { path: 'admin', component: AdminUserComponent },
]);
