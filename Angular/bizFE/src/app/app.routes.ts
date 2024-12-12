import { Routes } from '@angular/router';
import { HomeComponent } from './home.component';
import { BusinessesComponent } from './businesses.components';
import { BusinessComponent } from './business.component';
import { TestWSComponent } from './testWS.component';

export const routes: Routes = [
    {
        path: '',
        component: HomeComponent
    },
    {
        path: 'businesses',
        component: BusinessesComponent
    },
    {
        path: 'businesses/:id',
        component: BusinessComponent
    },
    {
        path: 'test',
        component: TestWSComponent
    }
];
