// const config = {
//   development: {
//     API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000'
//   },
//   production: {
//     API_BASE_URL: process.env.REACT_APP_API_URL || 'http://103.253.20.13:5000'
//   }
// };

// export default config[process.env.NODE_ENV || 'development']; 


// Trong docker-compose.prod.yml có thêm dòng [REACT_APP_API_URL=http://103.253.20.13:25037 
// - Override URL API mặc định trong config.js ] 
// TRƯỚC CHẠY ĐƯỢC GIỜ KHÔNG CHẠY ĐƯỢC -- do gửi file update prod.yml cho a Trúc 


const config = {
  development: {
    API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:25037'
  },
  production: {
    API_BASE_URL: process.env.REACT_APP_API_URL || 'http://103.253.20.13:25037'
  }
};

export default config[process.env.NODE_ENV || 'development']; 