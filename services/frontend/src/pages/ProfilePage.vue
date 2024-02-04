<template>
    <div class="card">
        <Panel >
            <template #header>
                <div class="flex w-full align-items-center flex-column gap-5">
                    <Avatar class="w-20rem h-20rem border-circle overflow-hidden" image="/images/avatar/default-avatar.png" size="xlarge" alt="Avatar"/>
                    <span class="flex flex-row gap-1">
                        <FileUpload chooseLabel="Загрузить" mode="basic" name="demo[]" url="/api/upload" accept="image/*" :maxFileSize="1000000" @upload="onUpload"/>
                        <Button v-if="false" outlined icon="pi pi-times"/>
                    </span>
                </div>
            </template>
            <Fieldset class="w-full" legend="Настройки профиля">
                <div class="flex flex-column gap-5">
                    <div class="flex flex-column gap-2">
                        <label for="username">Логин</label>
                        <InputText id="username" v-model="usernameValue" aria-describedby="username" />
                    </div>
                    <div class="flex flex-column gap-2">
                        <label for="email">Электронная почта</label>
                        <InputText id="email" v-model="emailValue" aria-describedby="email" />
                    </div>
                    <InputGroup>
                        <Password :feedback="false" v-model="passwordValue" disabled placeholder="*************" />
                        <Button icon="pi pi-pencil"/>
                        <Button v-if="false" icon="pi pi-check" severity="success"/>
                    </InputGroup>
                </div>
            </Fieldset>
            <template #footer>
                <div class="flex gap-3 mt-1">
                    <Button label="Отменить" severity="secondary" :disabled="true" outlined class="w-full" />
                    <Button label="Сохранить"  :disabled="true" class="w-full" />
                </div>
            </template>
        </Panel>
    </div>
</template>

<script setup>
import Button from 'primevue/button'
import Fieldset from 'primevue/fieldset';
import FileUpload from 'primevue/fileupload';
import Avatar from 'primevue/avatar';
import InputGroup from 'primevue/inputgroup';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Panel from 'primevue/panel';
</script>