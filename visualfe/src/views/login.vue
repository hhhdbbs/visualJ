<template>
  <div style="height:100%" class="d-flex justify-center">
    <v-card style="width:40%;height:50%;top:30%">
      <v-card-title>登录</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12">
            <v-text-field label="账号名" v-model="account"></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field label="密码" v-model="password"
            :append-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'"
            :type="show3 ? 'text' : 'password'"
            @click:append="show3 = !show3"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn depressed color="primary" @click="submit">
          登录
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
export default {
  name: "Login",
  date() {
    return {
      account: "",
      password: "",
      show3:false
    };
  },
  methods: {
    submit() {
      this.$axios
        .post(
          "/app/login/",
          this.qs.stringify({
            account: this.account,
            password: this.password
          }),
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
          }
        )
        .then(res => {
          const { result, isadmin } = res.data;
          if (!result) this.$message.error("登录失败");
          else {
            if (isadmin) {
              this.$router.push({ path: "/serverList" });
            } else {
              this.$router.push({ path: "/operatorList" });
            }
          }
        });
    }
  }
};
</script>
